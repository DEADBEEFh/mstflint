# Copyright (C) Jan 2020 Mellanox Technologies Ltd. All rights reserved.   
#                                                                           
# This software is available to you under a choice of one of two            
# licenses.  You may choose to be licensed under the terms of the GNU       
# General Public License (GPL) Version 2, available from the file           
# COPYING in the main directory of this source tree, or the                 
# OpenIB.org BSD license below:                                             
#                                                                           
#     Redistribution and use in source and binary forms, with or            
#     without modification, are permitted provided that the following       
#     conditions are met:                                                   
#                                                                           
#      - Redistributions of source code must retain the above               
#        copyright notice, this list of conditions and the following        
#        disclaimer.                                                        
#                                                                           
#      - Redistributions in binary form must reproduce the above            
#        copyright notice, this list of conditions and the following        
#        disclaimer in the documentation and/or other materials             
#        provided with the distribution.                                    
#                                                                           
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,         
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF        
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND                     
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS       
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN        
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN         
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE          
# SOFTWARE.                                                                 
# --                                                                        


#######################################################
# 
# SegmentCreator.py
# Python implementation of the Class SegmentCreator
# Generated by Enterprise Architect
# Created on:      14-Aug-2019 10:12:03 AM
# Original author: talve
# 
#######################################################
from segments.SegmentFactory import SegmentFactory
from utils import constants as cs


class SegmentCreator:
    """this class is responsible for splitting  the raw data to segments and creating
    segments objects.
    """
    def create(self, raw_data):
        """convert segments data into a segments objects by using SegmentFactory.
        """
        try:
            segments = []
            raw_data_segments_lst = self._parse_segments(raw_data)
            for raw_seg in raw_data_segments_lst:
                seg_type = '{:0b}'.format(raw_seg[cs.SEGMENT_TYPE_DWORD_LOCATION]).zfill(32)[cs.SEGMENT_TYPE_START: cs.
                                                                                             SEGMENT_TYPE_END]
                seg_type = hex(int(seg_type, 2))
                seg_type_for_create = SegmentCreator.get_seg_type_for_register_segments(seg_type)
                seg = SegmentFactory.create(seg_type_for_create, raw_seg)
                seg.resource_type = seg_type
                segments.append(seg)
        except Exception as e:
            raise Exception("Failed to create segments with error: {0}".format(e))
        return segments

    def _parse_segments(self, raw_data):
        """splitting  the raw data into segments
           raw data is represented as a list of dword's
        """
        splitted_segments = []
        try:
            while raw_data:
                raw_data_len = len(raw_data)
                # seg size specified in dwords
                seg_size = '{:0b}'.format(raw_data[cs.SEGMENT_SIZE_DWORD_LOCATION]).zfill(32)[cs.SEGMENT_SIZE_START: cs.
                                                                                              SEGMENT_SIZE_END]
                seg_size = int(seg_size, 2)
                seg_data = raw_data[:seg_size]
                splitted_segments.append(seg_data)
                raw_data = raw_data[seg_size:]
                if len(raw_data) == raw_data_len:
                    raise Exception("Error in segments parsing. raw_data didn't get smaller")

        except Exception as e:
            raise Exception("Failed to split segments with error: {0}".format(e))

        return splitted_segments

    @classmethod
    def is_resource_segment(cls, seg_type):
        """This method check if the segment type is a inside the interval of a resource segment
        """
        return cs.RESOURCE_DUMP_SEGMENT_TYPE_RESOURCE_MAX >= seg_type >= cs.RESOURCE_DUMP_SEGMENT_TYPE_RESOURCE_MIN

    @classmethod
    def get_seg_type_for_register_segments(cls, seg_type):
        """This method check if the segment type is a reference segment
           and return the right type of that segment.
        """
        if cls.is_resource_segment(seg_type):
            return cs.RESOURCE_DUMP_SEGMENT_TYPE_RESOURCE
        return seg_type