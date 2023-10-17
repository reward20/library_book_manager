from pathlib import WindowsPath
from collections import defaultdict
import shutil


class Lib_Manager:

    def __init__(self, input_path, output_path, type_file=None):
        self.dict_new_book = None
        if type_file is None:
            type_file = ["pdf", "djvu"]

        self.type_file = ["**/*." + t_file for t_file in type_file]
        self.in_path = WindowsPath(input_path)
        self.out_path = WindowsPath(output_path)
        self.copy_path = self.out_path.parent / "duplicated"
        self.del_path = self.out_path.parent / "exist"

        self.copy_book = defaultdict(dict)
        self.move_book = defaultdict(dict)

    def start_library_manager(self):
        self.__check_new_file()
        self.__move_lib_book()

    def __get_book(self, search_path):
        dict_book = defaultdict(dict)
        for type_book in self.type_file:
            for file in search_path.glob(type_book):
                dict_book[file.stem] = {"weight": file.stat().st_size, "path": file}
        return dict_book

    def __move_copy_book_look(self):
        # if duplicate folder is not exist
        if not self.copy_path.is_dir():
            self.copy_path.mkdir(parents=True)

        for k, name_file in enumerate(self.copy_book.keys()):
            file = self.copy_book[name_file]
            path_copy = self.copy_path / f"copy {k}"
            try:
                path_copy.mkdir()
            except FileExistsError:
                shutil.rmtree(path_copy)
                path_copy.mkdir()

            shutil.move(file["path"], path_copy)
            for copy_file in file["copy_path"]:
                shutil.move(copy_file, path_copy)

    def __get_new_file(self):
        """
        get an array of the new book of the form name-weight
        :return:
        array with new file
        """
        new_book = self.__get_book(self.in_path)
        keys_dict = list(new_book.keys())

        for i in range(len(keys_dict)):
            try:
                book = keys_dict.pop()
            except:
                break

            list_v = []
            for other_book in keys_dict:
                if new_book[book]["weight"] == new_book[other_book]["weight"]:
                    if book in self.copy_book:
                        self.copy_book[book]["copy_path"].append(new_book[other_book]["path"])
                        list_v.append(other_book)
                    else:
                        self.copy_book[book] = {"path": new_book[book]["path"],
                                                "copy_path": list([new_book[other_book]["path"]])}
                        list_v.append(other_book)
            for item in list_v:
                keys_dict.remove(item)


        # for book in keys_dict:
        #     for other_book in keys_dict:
        #
        #         if new_book[book]["weight"] == new_book[other_book]["weight"]:
        #             if book == other_book:
        #                 continue
        #             else:
        #                 if book in self.copy_book:
        #                     self.copy_book[book]["copy_path"].append(new_book[other_book]["path"])
        #                 else:
        #                     self.copy_book[book] = {"path": new_book[book]["path"],
        #                                             "copy_path": list([new_book[other_book]["path"]])}
        # keys_dict.remove(other_book)

        self.__move_copy_book_look()
        new_book = self.__get_book(self.in_path)
        return new_book

    def __get_old_file(self):
        """
        get an array of old books of the form name-weight
        :return:
        """
        return self.__get_book(self.out_path)

    def __check_new_file(self):
        """
        check for books that were not there
        :return:
        array of book to move
        """
        input_book = self.__get_new_file()
        store_book = self.__get_old_file()

        for name_new_book in input_book:
            new_file_bool = True
            for name_old_book in store_book:
                if name_new_book == name_old_book:
                    new_file_bool &= False
                    break
                elif input_book[name_new_book]["weight"] == store_book[name_old_book]["weight"]:
                    new_file_bool &= False
                    break
            if new_file_bool:
                self.move_book[name_new_book] = {"path": input_book[name_new_book]["path"]}

    def __move_lib_book(self):
        # move new book in library
        for new_book in self.move_book.keys():
            book = self.move_book[new_book]
            shutil.move(book["path"], self.out_path)
        other_book = self.__get_book(self.in_path)

        try:
            self.del_path.mkdir()
        except FileExistsError:
            pass

        for book in other_book:
            shutil.move(other_book[book]["path"], self.del_path)


    def __update_local_basedata(self):
        pass

    def __get_local_basedata(self):
        pass
