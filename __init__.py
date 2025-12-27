# -*- coding: utf-8 -*-
#
# Copyright (C) 2020, 2025 Bob Swift (rdswift)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.


from picard.plugin3.api import PluginApi


class ProcessLabelVariables:
    def __init__(self, api: PluginApi):
        self.api: PluginApi = api

    def process_labels(self, album_id, source_metadata, destination_metadata):
        # Test for valid metadata node.
        # The 'label-info' key should always be there.
        # This check is to avoid a runtime error if it doesn't exist for some reason.
        if 'label-info' in source_metadata:
            # Initialize variables to default values
            label_id_list = []
            label_name_list = []
            label_sort_name_list = []
            label_disambig_list = []
            label_count = 0
            catalog_number_list = []
            catalog_number_count = 0
            for label_info in source_metadata['label-info']:
                if 'catalog-number' in label_info and label_info['catalog-number']:
                    catalog_number_count += 1
                    catalog_number_list.append(label_info['catalog-number'])
                if 'label' in label_info:
                    label_count += 1
                    label_data = label_info['label']
                    label_id_list.append(label_data['id'] if 'id' in label_data and label_data['id'] else 'Unknown-Label-ID')
                    label_name_list.append(label_data['name'] if 'name' in label_data and label_data['name'] else 'Unknown Label Name')
                    label_sort_name_list.append(label_data['sort-name'] if 'sort-name' in label_data and label_data['sort-name'] else 'Unknown Label Sort Name')
                    label_disambig_list.append(label_data['disambiguation'] if 'disambiguation' in label_data else '')
            destination_metadata['~label_label_count'] = label_count
            destination_metadata['~label_catalog_count'] = catalog_number_count
            if label_id_list:
                destination_metadata['~label_ids_multi'] = label_id_list
            if label_name_list:
                destination_metadata['~label_names_multi'] = label_name_list
            if label_sort_name_list:
                destination_metadata['~label_sort_names_multi'] = label_sort_name_list
            if label_disambig_list:
                destination_metadata['~label_disambig_multi'] = label_disambig_list
            if catalog_number_list:
                destination_metadata['~label_catalog_multi'] = catalog_number_list
        else:
            # No valid metadata found.  Log as error.
            self.metadata_error(album_id, 'label-info')

    def make_label_vars(self, api, album, album_metadata, release_metadata):
        album_id = release_metadata['id'] if release_metadata else 'No Album ID'
        self.process_labels(album_id, release_metadata, album_metadata)

    def metadata_error(self, album_id, metadata_element):
        self.api.logger.error("{0!r}: Missing '{1}' in release metadata.".format(album_id, metadata_element,))


def enable(api: PluginApi):
    """Called when plugin is enabled."""

    plugin = ProcessLabelVariables(api)

    #######################
    #   Label Variables   #
    #######################

    api.register_script_variable(
        name="_label_ids_multi",
        documentation=api.tr(
            "variable.label_ids_multi",
            "All label IDs listed for the album, as a multi-value."
        )
    )

    api.register_script_variable(
        name="_label_names_multi",
        documentation=api.tr(
            "variable.label_names_multi",
            "All label names listed for the album, as a multi-value."
        )
    )

    api.register_script_variable(
        name="_label_sort_names_multi",
        documentation=api.tr(
            "variable.label_sort_names_multi",
            "All label names listed (sort name) for the album, as a multi-value."
        )
    )

    api.register_script_variable(
        name="_label_disambig_multi",
        documentation=api.tr(
            "variable.label_disambig_multi",
            "All label disambiguations listed for the album, as a multi-value."
        )
    )

    api.register_script_variable(
        name="_label_catalog_multi",
        documentation=api.tr(
            "variable.label_catalog_multi",
            "All label catalog numbers listed for the album, as a multi-value."
        )
    )

    api.register_script_variable(
        name="_label_label_count",
        documentation=api.tr(
            "variable.label_label_count",
            "Count of the number of labels listed for the album."
        )
    )

    api.register_script_variable(
        name="_label_catalog_count",
        documentation=api.tr(
            "variable.label_catalog_count",
            "Count of all catalog numbers listed for the album."
        )
    )

    # Register the plugin to run at a LOW priority so that other plugins that
    # modify the information can complete their processing and this plugin is
    # working with the latest updated data.
    api.register_album_metadata_processor(plugin.make_label_vars, priority=-100)
