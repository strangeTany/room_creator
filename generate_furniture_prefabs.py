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
    for i in range(len(room_ids)):
        purchase = room_ids[i]


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
    os.makedirs('./room')
    shutil.copy2('templates/Room_aN_RoomName_Window_template.xml', window_prefab)
    window = create_window_prefab()
    room_ids = get_purchase_ids()
    generate_choose_icons()

    print(window[0][4][7][2][1][0])
