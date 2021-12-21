import os
import argparse
import ibases


user_profile_path = os.environ['USERPROFILE']
ad_path = '\\AppData\\Local\\1C\\1cv8\\'
ls_path = '\\Local Settings\\Application Data\\1C\\1cv8\\'
ibases_path_rel = '\\AppData\\Roaming\\1C\\1CEStart\\ibases.v8i'
ibases_path = user_profile_path + ibases_path_rel


def section_from_line(line):
    if line.find('[') == 0:
        return line.replace('[', '').replace(']', '').strip()
    return None


def id_from_line(line):
    if line.find('ID=') == 0:
        return line.replace('ID=', '').strip()
    return None


def get_db_ids_from_ibases(ibases_path):
    db_ids = {}
    with open(ibases_path, 'r', encoding='utf-8') as f:
        section = None
        for line in f:
            new_section = section_from_line(line)
            if new_section:
                section = new_section
            else:
                db_id = id_from_line(line)
                if db_id:
                    db_ids[section] = db_id
    return db_ids


def clear_cache():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=str, required=True)
    args = parser.parse_args()

    # 'UTL_Terentev'
    db_name = args.d

    db_ids = get_db_ids_from_ibases(ibases_path)

    if db_name in db_ids:
        db_id = db_ids[db_name]
        print('ID={}'.format(db_id))

        path1 = user_profile_path + ad_path + db_id
        path2 = user_profile_path + ls_path + db_id

        if os.path.exists(path1):
            print(' .1. {}'.format(path1))
        if os.path.exists(path2):
            print(' .2. {}'.format(path2))


if __name__ == '__main__':
    clear_cache()
