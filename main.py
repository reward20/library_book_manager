import Lib_lab

if __name__ == '__main__':
    in_folder_path = r"D:\Проекты\library_manager\new_book"
    out_folder_path = r"D:\Проекты\library_manager\old_book"
    Lib_man = Lib_lab.Lib_Manager(in_folder_path, out_folder_path)
    Lib_man.start_library_manager()
