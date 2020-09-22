#
#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2019 Intel Corporation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow.core.framework import attr_value_pb2
from tensorflow.core.framework import node_def_pb2
from tensorflow.python.framework import dtypes
from intel_quantization.transform_graph.graph_transform_base import GraphTransformBase


class InsertLogging(GraphTransformBase):
    """
    Insert logging graph transformation.
    """
    op_output_type_mapping = {"RequantizationRange": [dtypes.float32.as_datatype_enum,
                                                      dtypes.float32.as_datatype_enum],
                              "RequantizationRangePerChannel": [dtypes.float32.as_datatype_enum,
                                                                dtypes.float32.as_datatype_enum],
                              "Max": [dtypes.float32.as_datatype_enum],
                              "Min": [dtypes.float32.as_datatype_enum]}

    def __init__(self, input_pb, ops=[], show_name=True, show_op=False,
                 first_n=-1, summarize=1024, message=""):
        super(InsertLogging, self).__init__(input_pb)

        self.parse_input_pb()
        self.ops = ops
        self.show_name = show_name
        self.show_op = show_op
        self.message = message
        self.first_n = first_n
        self.summarize = summarize
        self.output_name_index_mapping = {}
        self.input_rename = {}

    def _get_suffix(self, input_str):
        """
        Split the node name into two parts.
        Returns:
            Pure string name without suffix
            Index of the node
        """
        splitted_str = input_str.split(':')
        if len(splitted_str) < 2:
            return input_str, 0

        return splitted_str[0], splitted_str[-1]

    def _get_output_index_mapping(self):
        """
        Get the output_node_name and index mapping.
        """
        for node_name in self.node_mapping:
            for node_input in self.node_mapping[node_name].input:
                node_stripped_name, suffix = self._get_suffix(node_input)
                if node_stripped_name not in self.output_name_index_mapping:
                    self.output_name_index_mapping[node_stripped_name] = set()
                self.output_name_index_mapping[node_stripped_name].add(suffix)

    def _insert_node(self):
        """
        Insert the Print OP into the graph
        """
        for node_name in self.node_mapping:
            if node_name not in self.output_name_index_mapping or node_name.find("eightbit") == -1:
                continue

            if self.ops and self.node_mapping[node_name].op in self.ops:
                name_suffix = "__print__"
                print_node = node_def_pb2.NodeDef()
                print_node.op = "Print"
                print_node.name = node_name + name_suffix
                node_message = ''
                if self.show_op:
                    node_message += ';' + self.node_mapping[node_name].op + ';'
                if self.show_name:
                    node_message += ';' + print_node.name + ';'
                node_message += self.message

                print_node.attr["message"].s = node_message.encode()
                print_node.attr["first_n"].i = self.first_n
                print_node.attr["summarize"].i = self.summarize

                print_node.input.append(node_name + ":0")
                print_node.attr["T"].CopyFrom(
                    attr_value_pb2.AttrValue(type=self.op_output_type_mapping[self.node_mapping[node_name].op][0]))

                for index in sorted(self.output_name_index_mapping[node_name]):
                    print_node.input.append(node_name + ":" + str(index))

                print_node.attr["U"].list.CopyFrom(attr_value_pb2.AttrValue.ListValue(
                    type=self.op_output_type_mapping[self.node_mapping[node_name].op]))

                self.input_graph.node.extend([print_node])
                self.input_rename[node_name + ':0'] = print_node.name + ':0'

    def _rename_node(self):
        """
        Rename the original input node and connect to new added print node.
        """
        for node_name in self.node_mapping:
            for index, input_name in enumerate(self.node_mapping[node_name].input):
                if input_name in self.input_rename:
                    self.node_mapping[node_name].input[index] = self.input_rename[input_name]
                elif input_name + ':0' in self.input_rename:
                    self.node_mapping[node_name].input[index] = self.input_rename[input_name + ':0']

    def do_transformation(self):
        """
        Execute the insert logging transformation.
        :return: Transformed graph
        """
        self._get_output_index_mapping()
        self._insert_node()
        self._rename_node()

        return self.input_graph
