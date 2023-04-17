from collections.abc import Callable
import pandas as pd
import typing
from type import Comparable


def identity(elem: any) -> Comparable:
    return elem


def is_interval(interval: list | tuple, lower_boundry_included: bool = True, higher_boundry_included: bool = True) -> bool:
    if len(interval) != 2:
        return False
    if interval[1] < interval[0]:
        return False
    if interval[1] == interval[0] and not (lower_boundry_included and higher_boundry_included):
        return False
    return True


class SortedMap:
    def __init__(self, l: list, key: Callable[[any], Comparable] = identity, reverse: bool = False):
        self.reverse = reverse
        self.key = key
        self.sorted_list = sorted(l, reverse=self.reverse, key=self.key)
        self.length = len(self.sorted_list)
        self.map = {}
        for index, elem in enumerate(self.sorted_list):
            self.map[key(elem)] = index+1
        self.keys_df = pd.DataFrame(self.map.keys())

    def max_slice_indecies(self, max_key: Comparable) -> typing.Tuple[int, int]:
        if self.reverse:
            # sublist_keys = [k for k in self.map.keys() if k > max_key]
            sublist_keys = self.keys_df.loc[self.keys_df[0]
                                            > max_key][0].to_numpy()
            if sublist_keys.size == 0:
                return 0, self.length
            return self.map[sublist_keys.min()], self.length
        else:
            # sublist_keys = [k for k in self.map.keys() if k <= max_key]
            sublist_keys = self.keys_df.loc[self.keys_df[0]
                                            <= max_key][0].to_numpy()
            if sublist_keys.size == 0:
                return 0, 0
            return 0, self.map[sublist_keys.max()]

    def min_slice_indecies(self, min_key: Comparable) -> typing.Tuple[int, int]:
        if self.reverse:
            # sublist_keys = [k for k in self.map.keys() if k >= min_key]
            sublist_keys = self.keys_df.loc[self.keys_df[0]
                                            >= min_key][0].to_numpy()
            if sublist_keys.size == 0:
                return 0, 0
            return 0, self.map[sublist_keys.min()]
        else:
            # sublist_keys = [k for k in self.map.keys() if k < min_key]
            sublist_keys = self.keys_df.loc[self.keys_df[0]
                                            < min_key][0].to_numpy()
            if sublist_keys.size == 0:
                return 0, self.length
            return self.map[sublist_keys.max()], self.length

    def complement_indecies(self, indecies: typing.List[int] | typing.Tuple[int, int]) -> typing.Tuple[int, int]:
        if indecies[0] == 0:
            return indecies[1], self.length
        else:
            return 0, indecies[0]

    def lower_slice(self, max_key: Comparable, boundry_included: bool = True) -> list:
        if boundry_included:
            indecies = self.max_slice_indecies(max_key)
        else:
            indecies = self.complement_indecies(
                self.min_slice_indecies(max_key))
        return self.sorted_list[indecies[0]:indecies[1]].copy()

    def higher_slice(self, min_key: Comparable, boundry_included: bool = True) -> list:
        if boundry_included:
            indecies = self.min_slice_indecies(min_key)
        else:
            indecies = self.complement_indecies(
                self.max_slice_indecies(min_key))
        return self.sorted_list[indecies[0]:indecies[1]].copy()

    def band_slice(self, keys_interval: typing.List[Comparable] | typing.Tuple[int, int], lower_boundry_included: bool = True, higher_boundry_included: bool = True) -> list:
        if not is_interval(keys_interval, lower_boundry_included=lower_boundry_included, higher_boundry_included=higher_boundry_included):
            raise ValueError

        if higher_boundry_included:
            indecies_lower = self.max_slice_indecies(keys_interval[1])
        else:
            indecies_lower = self.complement_indecies(
                self.min_slice_indecies(keys_interval[1]))

        if lower_boundry_included:
            indecies_higher = self.min_slice_indecies(keys_interval[0])
        else:
            indecies_higher = self.complement_indecies(
                self.max_slice_indecies(keys_interval[0]))
        if self.reverse:
            return self.sorted_list[indecies_lower[0]:indecies_higher[1]].copy()
        else:
            return self.sorted_list[indecies_higher[0]:indecies_lower[1]].copy()


if __name__ == "__main__":
    sm = SortedMap([2, 10, 2, 1], reverse=False)
    print(sm.band_slice([1, 1]))
