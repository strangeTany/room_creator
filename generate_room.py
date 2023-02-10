import argparse
import os
import shutil
import xml
import xml.etree.ElementTree as ET
import random

parser = argparse.ArgumentParser()
parser.add_argument('room_name', type=str, help='Name of room')
parser.add_argument('areal', type=int, help='Number of areal')
args = parser.parse_args()

room_name = args.room_name
areal = args.areal
uids = []
# window_prefab = f'room/Room_a{areal}_{room_name}_Window.xml'
path_to_vso = f'/../../base1/Areal{areal}_Room_{room_name}/assets/Areal{areal}_Room_{room_name}/vso'
window_prefab = f'{path_to_vso}/Room_a{areal}_{room_name}_Window.xml'


def get_purchase_ids():
    tree = ET.parse(f'/../../base/assets/gameDataBase/rooms/Buildings/{room_name}.xml')
    root = tree.getroot()
    room_skins = root[1][0][0][0]
    room_ids = dict()
    for child in room_skins:
        if child.tag == 'decorPurchases':
            purchase_id = child[0].attrib['id'][len(room_name) + 1:]
            if purchase_id != '':
                room_ids[purchase_id] = []
                for skin in child[0]:
                    can_be_selected = skin[0].attrib['canBeSelected']
                    can_be_selected = True if can_be_selected == 'true' else False
                    skin_id = skin[0].attrib['id'][len(room_name) + 1:]
                    skin_id = 'empty' if skin_id == '' else skin_id
                    room_ids[purchase_id].append((can_be_selected, skin_id))
    return room_ids


def get_uid():
    uid = random.randint(100000000, 999999999)
    if uid not in uids:
        uids.append(uid)
        return uid
    else:
        get_uid()


def generate_furniture_prefabs():
    os.makedirs(f'{path_to_vso}/FurniturePrefabs')
    shutil.copy2('templates/Room_aN_RoomName_Furniture_template.xml',
                 f'{path_to_vso}/Room_a{areal}_{room_name}_Furniture.xml')
    furniture_uid = str(get_uid())
    link_object(furniture_uid, f'Room_a{areal}_{room_name}_Furniture', 'Background', window.getroot()[0][4][4])
    window.getroot()[0][4][0][0][3].attrib['path'] = furniture_uid
    for i in range(len(room_ids)):
        purchase = list(room_ids)[i]
        shutil.copy2('templates/FurniturePrefab_template.xml',
                     f'{path_to_vso}/FurniturePrefabs/{room_name}_{purchase}.xml')
        tree = ET.parse(f'{path_to_vso}/FurniturePrefabs/{room_name}_{purchase}.xml')
        root = tree.getroot()
        root[0].attrib["name"] = f'{i}_{purchase}'
        root[0][0][0][1].attrib["entityId"] = str(get_uid())
        purchase_uid = str(get_uid())
        purchase_obj_id = str(get_uid())
        purchase_path = f'{furniture_uid}/{purchase_obj_id}/{purchase_uid}'
        root[0][2].attrib['entityId'] = purchase_uid
        redesign_node = False
        redesign_uid = 0
        redesign_path = 0
        for j in range(len(room_ids[purchase])):
            skin = room_ids[purchase][j]
            skin_uid = create_empty_img(root, j)
            skin_path = f'{furniture_uid}/{purchase_obj_id}/{skin_uid}'
            if skin[0] and not redesign_node:
                redesign_node = True
                redesign_uid = str(get_uid())
                redesign_path = f'{furniture_uid}/{purchase_obj_id}/{redesign_uid}'
            add_purchase(skin_path, purchase_path, redesign_path, purchase, skin[1], skin[0])
        if redesign_node:
            create_redesign_node(root, redesign_uid)
        tree.write(f'{path_to_vso}/FurniturePrefabs/{room_name}_{purchase}.xml')
        furniture_tree = ET.parse(f'{path_to_vso}/Room_a{areal}_{room_name}_Furniture.xml')
        furniture = furniture_tree.getroot()[0]
        link_object(purchase_obj_id, f'{room_name}_{purchase}', f'{i}_{purchase}', furniture)
        furniture_tree.write(f'{path_to_vso}/Room_a{areal}_{room_name}_Furniture.xml')


def link_object(obj_id, linked_object, node_name, root):
    ET.SubElement(root, 'children')
    root[-1].attrib['name'] = node_name
    ET.SubElement(root[-1], 'link')
    root[-1][0].attrib['objId'] = obj_id
    ET.SubElement(root[-1][0], 'id')
    root[-1][0][0].attrib['id'] = linked_object
    root[-1][0][0].attrib['id..editor..ref'] = "assetType@sceneObject"
    ET.SubElement(root[-1], 'transform')
    ET.SubElement(root[-1], 'uid')
    root[-1][-1].attrib['entityId'] = str(get_uid())


def create_anchored_element(root):
    ET.SubElement(root, 'behaviours')
    anchored_element = root[0]
    anchored_element.attrib['type'] = "anchoredElement"
    ET.SubElement(anchored_element, 'ptr')
    ET.SubElement(anchored_element[0], 'horizontalAnchor')
    anchored_element[0][0].attrib['nrp_1'] = '0.5'
    ET.SubElement(anchored_element[0], 'normalizedPivot')
    anchored_element[0][1].attrib['x'] = '0.5'
    anchored_element[0][1].attrib['y'] = '0.5'
    ET.SubElement(anchored_element[0], 'uid')
    anchored_element[0][2].attrib['entityId'] = str(get_uid())
    ET.SubElement(anchored_element[0], 'verticalAnchor')
    anchored_element[0][3].attrib['nrp_1'] = '0.5'


def create_empty_img(root, idx):
    ET.SubElement(root[0], 'children')
    img_node = root[0][idx + 3]
    img_node.attrib['name'] = f'img_{idx}'
    img_node.attrib['visibility'] = f'false'
    create_anchored_element(img_node)
    ET.SubElement(img_node, 'transform')
    ET.SubElement(img_node, 'uid')

    img_uid = str(get_uid())
    img_node[2].attrib['entityId'] = img_uid
    return img_uid


def create_redesign_node(root, uid):
    ET.SubElement(root[0], 'children')
    redesign_node = root[0][-1]
    redesign_node.attrib['name'] = 'redesign_spot'

    create_anchored_element(redesign_node)

    ET.SubElement(redesign_node, 'behaviours')
    redesign_node[1].attrib['type'] = 'RoomDesignEditIconAngle'
    ET.SubElement(redesign_node[1], 'ptr')
    ET.SubElement(redesign_node[1][0], 'uid')
    redesign_node[1][0][0].attrib['entityId'] = str(get_uid())

    ET.SubElement(redesign_node, 'sorting')
    redesign_node[2].attrib['type'] = 'priority'
    ET.SubElement(redesign_node[2], 'ptr')
    redesign_node[2][0].attrib['priorityValue'] = '302'
    ET.SubElement(redesign_node[2][0], 'uid')
    redesign_node[2][0][0].attrib['entityId'] = str(get_uid())

    ET.SubElement(redesign_node, 'transform')
    ET.SubElement(redesign_node, 'uid')
    redesign_node[-1].attrib['entityId'] = uid


def add_purchase(skin_path, purchase_path, redesign_path, purchase, skin, is_redesign):
    main_behaviour = window.getroot()[0][4][0][0]
    ET.SubElement(main_behaviour, 'purchaseViews')
    main_behaviour[-1].attrib['type'] = "purchaseView"
    ET.SubElement(main_behaviour[-1], 'ptr')
    main_behaviour[-1][0].attrib['autoCreateButton'] = "false"
    main_behaviour[-1][0].attrib['purchaseId'] = f'{room_name}_{purchase}'
    main_behaviour[-1][0].attrib['purchaseSkin'] = f'{room_name}_{skin}'
    ET.SubElement(main_behaviour[-1][0], 'backgroundIcon')
    ET.SubElement(main_behaviour[-1][0], 'ref')
    main_behaviour[-1][0][-1].attrib['path'] = skin_path
    ET.SubElement(main_behaviour[-1][0], 'selectedRef')
    main_behaviour[-1][0][-1].attrib['path'] = purchase_path
    if is_redesign:
        ET.SubElement(main_behaviour[-1][0], 'pinRef')
        main_behaviour[-1][0][-1].attrib['path'] = redesign_path


def generate_choose_icons():
    os.makedirs(f'{path_to_vso}/ChoosePanelPrefabs')
    choose_panel = window.getroot()[0][4][7][2][1][0]
    for purchase in room_ids:
        for skin in room_ids[purchase]:
            if skin[0]:
                icon_name = f'Icon_{room_name}_{purchase}{skin[1][-1]}'
                shutil.copy2('templates/Icon_Room_template.xml',
                             f'{path_to_vso}/ChoosePanelPrefabs/{icon_name}.xml')
                ET.SubElement(choose_panel, 'viewInfo')
                choose_panel[-1].attrib["type"] = "skinSelectorViewInfo"
                ET.SubElement(choose_panel[-1],
                              f'ptr id = "{room_name}_{purchase}" prefabId = "{icon_name}" skin = "{room_name}_{skin[1]}"')


def create_window_prefab():
    tree = ET.parse(window_prefab)
    root = tree.getroot()
    root[0].attrib['name'] = f'Room_a{areal}_{room_name}_Window'
    return tree


if __name__ == '__main__':
    shutil.copy2('templates/Room_aN_RoomName_Window_template.xml', window_prefab)
    window = create_window_prefab()
    room_ids = get_purchase_ids()
    generate_furniture_prefabs()
    generate_choose_icons()
    window.write(window_prefab)

    print()
