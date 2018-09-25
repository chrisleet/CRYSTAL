import matplotlib.pyplot as plt
import numpy as np

import utility.utility as utility


# Clusters are denoted by the 2-tuple (start_px, end_px). This set of globals
# notes that the index of the start pixel, given by ST_IND, is 0, and the 
# index of the finish pixel, given by END_IND, is 1.
global ST_IND
ST_IND = 0
global END_IND
END_IND = 1

def identify_clusters(shards):

    '''
    Identifies flagged clusters of telluric pixels.
    '''

    for shard in shards.itervalues():
        for tel_flags, clusters in zip([shard.w_tel, shard.z_tel], 
                                       [shard.w_clusters, shard.z_clusters]):
            cluster_start = None
            for i in range(shard.hi_px - shard.lo_px):
                if tel_flags[i] and cluster_start is None: 
                    cluster_start = i
                elif (not tel_flags[i] or i+1 == shard.hi_px) and cluster_start is not None:
                    clusters.append([cluster_start, i-1])
                    cluster_start = None
                    
def remove_1_and_2_pixel_clusters(shards):

    '''
    Removes 1 or 2 pixel telluric clusters.
    '''

    for shard in shards.itervalues():
        for clusters in [shard.w_clusters, shard.z_clusters]:
            clusters_copy = clusters[:]  #Separate list for iteration
            for cluster in clusters_copy:
                if cluster[END_IND] - cluster[ST_IND] + 1 < 3:
                    clusters.remove(cluster)

def remove_non_trough_clusters(shards, config):

    '''
    Removes clusters not in the shape of a trough.

    To avoid having to analyze each spectrum in a cluster seperately, the 
    clusters are coadded, and trough detection applied to the coadded cluster.
    '''

    for shard in shards.itervalues():
        coadded_x, coadded_log_y = utility.coadd_spectrum(shard)
        for clusters in [shard.w_clusters, shard.z_clusters]:
            clusters_copy = clusters[:]
            for cluster in clusters_copy:
                if not is_cluster_a_trough(coadded_x[cluster[ST_IND]-1:cluster[END_IND]+2], 
                                           coadded_log_y[cluster[ST_IND]-1:cluster[END_IND]+2], 
                                           config):
                    clusters.remove(cluster)
            


def is_cluster_a_trough(px_x, px_y, config):

    '''
    Takes a cluster of pixels, determines whether it is a trough.

    Each cluster of pixels is analyzed to determine whether it is a trough
    using a gradient based trough finding algorithm. This algorithm is based on
    the observation that the gradient of a trough starts negative, flips to
    being positive at its peak, and then returns to an overall gradient of 0. 
    
    We therefore mark a cluster as a peak if it contains a pixel below the
    gradient threshold followed by a pixel after the gradient threshold.

    Parameters
    ----------
    px: list (float)
         A list of the signal intensities of the pixels in the cluster.
    '''

    grad_threshold = config["threshold_gradient"]
    deltas = px_y[1:] - px_y[:-1]
    blocked_deltas = deltas[:-1] + deltas[1:]
    
    was_below_threshold = False
    has_peak = False
    for i in blocked_deltas:
        if i < -grad_threshold:
            was_below_threshold = True
        elif i > grad_threshold and was_below_threshold:
            has_peak = True
        
    # This plot is useful if you are debugging the peak finding algorithm.
    show_cluster_analysis = False
    if show_cluster_analysis:
        fig = plt.figure(facecolor="white")
        plt.plot(px_x, px_y, color="k")
        if has_peak:
            plt.plot(px_x[1:-1], blocked_deltas, color="g")
        else:
            plt.plot(px_x[1:-1], blocked_deltas, color="r")
        plt.axhline(grad_threshold)
        plt.axhline(-grad_threshold)
        plt.show()

    return has_peak

def remove_isolated_clusters(shards):

    '''
    Removes any cluster < 5A away from another cluster.
    '''

    for shard in shards.itervalues():
        coadded_x, coadded_log_y = utility.coadd_spectrum(shard)
        for clusters in [shard.w_clusters, shard.z_clusters]:
            clusters_copy = clusters[:]
            for i in range(len(clusters_copy)):
                # If there is a cluster < 5A to the left
                if i > 0 and (coadded_x[clusters_copy[i][ST_IND]] \
                        - coadded_x[clusters_copy[i-1][END_IND]]) <= 5:
                    pass
                # If there is a cluster < 5A to the right
                elif i < len(clusters_copy)-1 and (coadded_x[clusters_copy[i+1][ST_IND]] \
                        - coadded_x[clusters_copy[i][END_IND]]) <= 5:
                    pass
                else:
                    clusters.remove(clusters_copy[i])

def expand_clusters(shards):

    '''
    Expands each cluster by 1 pixel to pick up pixels in its tail
    '''
    for shard in shards.itervalues():
        for clusters in [shard.w_clusters, shard.z_clusters]:
            for i in range(len(clusters)):
                if clusters[i][ST_IND] > 0:
                    clusters[i][ST_IND] -= 1
                if clusters[i][END_IND] < shard.hi_px - shard.lo_px:
                    clusters[i][END_IND] += 1

def resolve_same_class_overlapping_clusters(shards):

    '''
    Merge any pair of overlapping same class clusters
    '''

    for shard in shards.itervalues():
        for clusters in [shard.w_clusters, shard.z_clusters]:
            i = 0
            while i < len(clusters) - 1:
                if clusters[i+1][ST_IND] <= clusters[i][END_IND]:
                    clusters[i][END_IND] = clusters[i+1][END_IND]
                    clusters.remove(clusters[i+1])
                else:
                    i += 1
                
def find_diff_class_overlapping_clusters(w_clusters, z_clusters):
    '''
    Returns overlapping diff class cluster pair if present, and None otherwise.
    '''

    for w_i in w_clusters:
        for z_i in z_clusters:
            if not ((w_i[ST_IND] < z_i[ST_IND] and w_i[END_IND] < z_i[ST_IND])
                    or (z_i[END_IND] < w_i[ST_IND] and z_i[END_IND] < w_i[ST_IND])):
                return (w_i, z_i)
    return None

def resolve_diff_class_overlapping_clusters(shards):
    
    '''
    Resolve overlapping water and non-water clusters.
    '''
    
    for shard in shards.itervalues():
        
        # While there are overlapping clusters left, removing them as follows
        while find_diff_class_overlapping_clusters(shard.w_clusters, shard.z_clusters) != None:
            w_i, z_i = find_diff_class_overlapping_clusters(shard.w_clusters, shard.z_clusters)
            
            # 1) If one cluster is a subset of another cluster, remove it
            if z_i[ST_IND] <= w_i[ST_IND] and w_i[END_IND] <= z_i[END_IND]:
                shard.w_clusters.remove(w_i)
                continue
            elif w_i[ST_IND] <= z_i[ST_IND] and z_i[END_IND] <= w_i[END_IND]:
                shard.z_clusters.remove(z_i)
                continue

            # 2) Identify the left and right clusters
            if w_i[ST_IND] < z_i[ST_IND]:
                L, L_PCCs = w_i, shard.w_PCCs
                R, R_PCCs = z_i, shard.z_PCCs
            else:
                L, L_PCCs = z_i, shard.z_PCCs 
                R, R_PCCs = w_i, shard.w_PCCs
    
            # 3) Now, the two clusters in their overlap region look like this:
            #
            #             L cluster | overlap region | R cluster
            #
            # We now check to see if the pixel adjacent to the L cluster has
            # a bigger L_PCC than R_PCC. If it does, we expand the L cluster's
            # bound by 1, and we check the next pixel, until we either reach
            # the end of the overlap region or we arrive at a pixel with a 
            # bigger R_PCC than L_PCC. We then repeat the process for the 
            # L_PCC. At the end of this step, the boundary between the L
            # cluster and the overlap region is a pixel with bigger R_PCC than
            # L_PCC, and vice versa.
            #
            # As an example, denoting pixels where L_PCC > R_PCC as L and the
            # reverse as R, if the pixels in the clusters and overlap region 
            # initially look like this:
            #
            #             L cluster [ overlap region ] R cluster
            #             LLLLLLLLLL[LLLLRRLRLLRLRRRR]RRRRRRRRR
            # 
            # then, they now look like this:
            #             L cluster     [ overlap]    R cluster
            #             LLLLLLLLLLLLLL[RRLRLLRL]RRRRRRRRRRRRR
            #
            # The overlap region is bounded to the left by a "R" pixel and
            # to the right by a "L" pixel.

            #Shrink the overlap from the left
            while L[END_IND] >= R[ST_IND] and L_PCCs[R[ST_IND]] >= R_PCCs[R[ST_IND]]:
                R[ST_IND] += 1

            #Shrink the overlap from the right
            while L[END_IND] >= R[ST_IND] and R_PCCs[L[END_IND]] >= L_PCCs[L[END_IND]]:
                L[END_IND] -= 1

            # 4) Now, an assignment is made for the overlap region, if one exists. If the overlap
            # region is >75% R pixels, it is assigned to the R cluster. If the overlap region is 
            # >75% L pixels, it is assigned to the L cluster. Otherwise, it is marked as a 
            # composite region
            if L[END_IND] >= R[ST_IND]:
                L_px, R_px = 0, 0
                for i in range(R[ST_IND], L[END_IND] + 1):
                    if L_PCCs[i] >= R_PCCs[i]:
                        L_px += 1
                    else:
                        R_px += 1
                if (L_px / float(L_px + R_px)) >= 0.75:
                    R[ST_IND] = L[END_IND] + 1
                elif (R_px / float(L_px + R_px)) >= 0.75:
                    L[END_IND] = R[ST_IND] - 1
                else:
                    composite_cluster = [R[ST_IND], L[END_IND]]
                    L[END_IND] = composite_cluster[ST_IND] - 1
                    R[ST_IND] = composite_cluster[END_IND] + 1
                    shard.c_clusters.append(composite_cluster)
        
        #end while
        if find_diff_class_overlapping_clusters(shard.w_clusters, shard.z_clusters) != None:
            raise Exception("Cluster resolution finished with overlapping w and z clusters")

        if find_diff_class_overlapping_clusters(shard.w_clusters, shard.c_clusters) != None:
            raise Exception("Cluster resolution finished with overlapping w and c clusters")

        if find_diff_class_overlapping_clusters(shard.z_clusters, shard.c_clusters) != None:
            raise Exception("Cluster resolution finished with overlapping z and c clusters")

        
