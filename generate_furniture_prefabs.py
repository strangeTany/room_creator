import os
import shutil
import xml
import xml.etree.ElementTree as ET
import random

room_name = 'MountainChalet'
areal = 3
uids = []
window_prefab = f'room/Room_a{areal}_{room_name}_Window.xml'


def get_purchase_ids():
    tree = ET.parse(f'vso/{room_name}.xml')
    root = tree.getroot()
    room_skins = root[1][0][0][0]
    room_ids = dict()
    for child in room_skins:
        if child.tag == 'decorPurchases':
            purchase_id = child[0].attrib['id'][len(room_name) + 1:]
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
    os.makedirs('./room/FurniturePrefabs')
    for i in range(len(room_ids)):
        purchase = list(room_ids)[i]
        shutil.copy2('templates/FurniturePrefab_template.xml',
                     f'room/FurniturePrefabs/{room_name}_{purchase}.xml')
        tree = ET.parse(f'room/FurniturePrefabs/{room_name}_{purchase}.xml')
        root = tree.getroot()
        root[0].attrib["name"] = f'{i}_{purchase}'
        root[0][0][0][1].attrib["entityId"] = str(get_uid())
        purchase_uid = str(get_uid())
        root[0][2].attrib['entityId'] = purchase_uid
        redesign_node = False
        redesign_uid = 0
        for j in range(len(room_ids[purchase])):
            skin = room_ids[purchase][j]
            skin_uid = create_empty_img(root, j)
            if skin[0] and not redesign_node:
                redesign_node = True
                redesign_uid = str(get_uid())
        if redesign_node:
            create_redesign_node(root, redesign_uid)
        tree.write(f'room/FurniturePrefabs/{room_name}_{purchase}.xml')


def create_anchored_element(root):
    ET.SubElement(root, 'behaviours')
    anchored_element = root[0]
    anchored_element.attrib['type'] = "anchoredElement"
    ET.SubElement(anchored_element, 'ptr')
    anchored_element[0].attrib['attachToParentInStart'] = 'true'
    anchored_element[0].attrib['autoAttachToParent'] = 'true'
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


def generate_choose_icons():
    os.makedirs('./room/ChoosePanelPrefabs')
    choose_panel = window.getroot()[0][4][7][2][1][0]
    for purchase in room_ids:
        for skin in room_ids[purchase]:
            if skin[0]:
                icon_name = f'Icon_{room_name}_{purchase}{skin[1][-1]}'
                shutil.copy2('templates/Icon_Room_template.xml',
                             f'room/ChoosePanelPrefabs/{icon_name}.xml')
                ET.SubElement(choose_panel, 'viewInfo')
                choose_panel[-1].attrib["type"] = "skinSelectorViewInfo"
                ET.SubElement(choose_panel[-1],
                              f'ptr id = "{room_name}_{purchase}" prefabId = "{icon_name}" skin = "{room_name}_{skin[1]}"')


def create_window_prefab():
    tree = ET.parse(f'room/Room_a{areal}_{room_name}_Window.xml')
    root = tree.getroot()
    root[0].attrib['name'] = window_prefab[-4]
    return tree


if __name__ == '__main__':
    # os.makedirs('./room')
    # shutil.copy2('templates/Room_aN_RoomName_Window_template.xml', window_prefab)
    # window = create_window_prefab()
    room_ids = get_purchase_ids()
    generate_furniture_prefabs()
    # generate_choose_icons()

    print()
