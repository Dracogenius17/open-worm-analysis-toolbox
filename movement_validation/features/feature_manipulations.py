# -*- coding: utf-8 -*-
"""



"""

from .. import utils
from . import generic_features

import copy

import numpy as np


def _expand_event_features(old_features,e_feature,m_masks,num_frames):
    """
        event 
        - at some point we need to filter events :/
        - When not signed, only a single value
        - If signed then 4x, then we compute all, absolute, positive, negative
    """
    
    cur_spec = e_feature.spec
    
    #TODO: Let's filter partials (0 and n_frames)
    #I'd like to push this to the feature method
    #cur_data = e_feature.get_full_values
    cur_data = e_feature.value

    # Remove the NaN and Inf entries
    all_data = utils.filter_non_numeric(cur_data)
    
    data_entries = {}
    data_entries['all'] = all_data
    if cur_spec.is_signed:
        data_entries['absolute'] = np.absolute(all_data)
        data_entries['positive'] = all_data[all_data >= 0]
        data_entries['negative'] = all_data[all_data <= 0]
    
    #JAH at this point
    import pdb
    pdb.set_trace()
    
    #This should eventually change I think ...
    parent_name = generic_features.get_parent_feature_name()    
    
    if cur_spec.is_signed    
    
    
    
    d_masks = {}
    d_masks['all'] = good_data_mask
    if cur_spec.is_signed:
        d_masks["absolute"] = good_data_mask
        d_masks["positive"] = cur_data >= 0 #bad data will be false
        d_masks["negative"] = cur_data <= 0 #bad data will be false
            

    
    pass

def _expand_movement_features(m_feature,m_masks,num_frames):
    """
    Movement features are expanded as follows:
        - if not signed, then we have 4x based on how the worm is moving\
            - all
            - forward
            - paused
            - backward
        - if signed, then we have 16x based on the features values and 
        based on how the worm is moving
        
    *All NaN values are removed
    
    """

    #feature names
    

    motion_types = ['all', 'forward', 'paused', 'backward']
    data_types = ['all', 'absolute', 'positive', 'negative']
    
    cur_spec = m_feature.spec
    cur_data = m_feature.value

    good_data_mask = ~utils.get_non_numeric_mask(cur_data).flatten()
    
    d_masks = {}
    d_masks['all'] = good_data_mask
    if cur_spec.is_signed:
        d_masks["absolute"] = good_data_mask
        d_masks["positive"] = cur_data >= 0 #bad data will be false
        d_masks["negative"] = cur_data <= 0 #bad data will be false       
    
    # Now let's create 16 histograms, for each element of
    # (motion_types x data_types)
    
    new_features = []
    for cur_motion_type in motion_types:

        #We could get rid of this if we don't care about the order
        #OR if we use an ordered dict ...
        if cur_spec.is_signed:
            end_type_index = 4
        else:
            end_type_index = 1
            
        for cur_data_type in data_types[:end_type_index]:
            new_feature = _create_new_movement_feature(m_feature,m_masks,d_masks,cur_motion_type,cur_data_type)
            new_features.append(new_feature)
    
    return new_features

def _create_new_movement_feature(feature,m_masks,d_masks,m_type,d_type):
    """
    
    Parameters
    ----------
    m_type : string
        Movement type
    d_type : string
        Data type
    """
    
    #Spec adjustment
    #---------------    
    
    
    FEATURE_NAME_FORMAT_STR = '%s.%s_data_with_%s_movement'
    
    cur_mask = m_masks[m_type] & d_masks[d_type]
    temp_feature = feature.copy()
    temp_spec = feature.spec.copy()
    temp_spec.type = 'expanded_movement'
    temp_spec.is_time_series = False
    temp_spec.name = FEATURE_NAME_FORMAT_STR % (temp_spec.name,d_type,m_type)
    
    #We might want to change this to load from the spec
    temp_feature.name = temp_spec.name
    #display_name?
    #short_display_name?
    #
    #has_zero_bin => stays the same
    #is_signed => maybe ...
    temp_spec.is_signed = temp_spec.is_signed and d_type == 'all'
    if d_type == 'absolute':
        temp_feature.value = np.absolute(feature.value[cur_mask])
    else:
        temp_feature.value = feature.value[cur_mask]
        
    temp_feature.spec = temp_spec
    
    return temp_feature


def expand_mrc_features(old_features):
    """
    Feature Expansion:
    ------------------
    simple - no expansion
    movement 
        - if not signed, then we have 4x based on how the worm is moving\
            - all
            - forward
            - paused
            - backward
        - if signed, then we have 16x based on the features values and 
        based on how the worm is moving
    event 
        - at some point we need to filter events :/
        - When not signed, only a single value
        - If signed then 4x, then we compute all, absolute, positive, negative
        
    Outline
    -------
    Return a new set of features in which the specs have been appropriately
    modified (need to implement a deep copy)
    """

    #Motion of the the worm's body
    motion_types = ['all', 'forward', 'paused', 'backward']
    #Value that the current feature is taking on
    data_types = ['all', 'absolute', 'positive', 'negative']

    motion_modes = old_features.get_feature('locomotion.motion_mode').value    
    
    num_frames = len(motion_modes)
    
    move_mask = {}
    move_mask["all"]      = np.ones(num_frames, dtype=bool)
    move_mask["forward"]  = motion_modes == 1
    move_mask["backward"] = motion_modes == -1
    move_mask["paused"]   = motion_modes == 0


    all_features = []
    for cur_feature in old_features:
        
        cur_spec = cur_feature.spec
        
        if cur_spec.type == 'movement':
            all_features.extend(_expand_movement_features(cur_feature,move_mask,num_frames))
        #elif cur_spec.type == 'simple':
        #    all_features.append(copy.deepcopy(cur_feature))
        elif cur_spec.type == 'event':
            all_features.extend(_expand_event_features(old_features,cur_feature,move_mask,num_frames))
        else:
            all_features.extend(copy.deepcopy(cur_feature))
            
            
    #TODO: Return new features container with all_features attached
