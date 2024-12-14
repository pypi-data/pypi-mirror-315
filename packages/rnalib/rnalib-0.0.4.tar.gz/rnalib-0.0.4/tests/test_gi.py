"""
Tests for GenomicInterval class
"""

from itertools import product, pairwise

import HTSeq
import pytest

import rnalib as rna
from rnalib import gi, GI

assert rna.__RNALIB_TESTDATA__ is not None, (
    "Please set rnalib.__RNALIB_TESTDATA__ variable to the testdata " "directory path"
)


def merge_result_lists(lst):
    """helper function"""
    l1, l2 = zip(*lst)
    m = GI.merge(list(l1))
    seq = "".join([str(x) for x in l2])
    return m, seq


def from_str(s):
    return [gi(x) for x in s.split(",")]


def test_show_init_performance():
    import timeit

    print(
        "GI",
        timeit.timeit('gi("chr1", 1, 10)', setup="from rnalib import gi", number=10000),
    )
    print("standard tuple", timeit.timeit('("chr1", 1, 10)', number=10000))


def test_loc_simple():
    # simple tests on single chrom
    d = {
        "a": gi("chr1:1-10"),
        "b": gi("chr1:5-20"),
        "c": gi("chr1:1-20"),
        "d": gi("chr1:15-20"),
    }
    assert d["a"] < d["b"]
    assert d["a"] != d["b"]
    assert d["b"] != d["a"]
    assert d["a"] == d["a"]
    assert d["a"].overlaps(d["b"])
    assert not d["a"].overlaps(d["d"])
    assert list(sorted(d.values())) == [d["a"], d["c"], d["b"], d["d"]]
    assert list(reversed(sorted(d.values()))) == list(
        reversed([d["a"], d["c"], d["b"], d["d"]])
    )
    # stranded
    d["a+"] = d["a"].get_stranded("+")
    assert (
        (d["a+"] < d["b"])
        and (d["d"] > d["a+"])
        and (not d["a+"] == d["b"])
        and (d["a+"] != d["b"])
    )
    # stranded
    a = gi("chr1", 1, 10)
    assert a.get_stranded("+") == a.get_stranded("+")
    assert a.get_stranded("+") == a.get_stranded("-").get_stranded("+")
    assert a.get_stranded("+") != a.get_stranded("-")
    assert a.get_stranded("+") != a.get_stranded("-").get_stranded("-")
    # frozen
    with pytest.raises(AttributeError):
        a.start = 2
    with pytest.raises(AttributeError):
        a.chromosome = "chr" + a.chromosome


def test_loc_overlaps():
    # Some overlap tests
    # .........1........  ....2......
    # |-a-|
    #     |-b-|
    #   |-c-|
    #           |-d-|
    #                         |-e-|
    #                     |-feature--------|
    d = {
        "a": gi("1", 1, 10),
        "b": gi("1", 11, 20),
        "c": gi("1", 5, 15),
        "d": gi("1", 30, 40),
        "e": gi("2", 21, 30),
        "feature": gi("2", 1, 50),
    }
    d_plus = {x: d[x].get_stranded("+") for x in d}
    d_minus = {x: d[x].get_stranded("-") for x in d}

    assert not d["a"].overlaps(d["b"])
    assert d["a"].overlaps(d["c"])
    assert d["c"].overlaps(d["a"])
    assert d["b"].overlaps(d["c"])
    assert d["e"].overlaps(d["feature"])
    assert d["feature"].overlaps(d["e"])
    # is_adjacent
    assert d["a"].is_adjacent(d["b"])
    # wrong chrom: no overlap
    for x, y in product(["a", "b", "c", "d"], ["e", "feature"]):
        assert not d[x].overlaps(d[y])
        assert not d[x].is_adjacent(d[y])
    # wrong strand: no overlap
    for x in d.keys():
        assert not d[x].overlaps(d_plus[x], strand_specific=True)
        assert not d_minus[x].overlaps(d_plus[x], strand_specific=True)
        assert not d[x].is_adjacent(d_plus[x], strand_specific=True)
        assert not d_minus[x].is_adjacent(d_plus[x], strand_specific=True)


def test_loc_overlaps_unrestricted():
    d = {
        "a": gi("1", 1, 10),
        "b": gi("1", 11, 20),
        "c": gi("1", 5, 15),
        "d": gi("1", 30, 40),
        "e": gi("2", 21, 30),
        "feature": gi("2", 1, 50),
    }
    # unrestricted intervals
    assert d["a"].overlaps(gi("1", None, None))
    assert d["a"].overlaps(gi("1", 8, None))
    assert not d["a"].overlaps(gi("1", 11, None))
    assert d["a"].overlaps(gi(None, 1, None))


def test_loc_merge():
    # Some merging tests
    # .........1........  ....2......
    # |-a-|
    #     |-b-|
    #   |-c-|
    #           |-d-|
    #                         |-e-|
    #                     |-feature--------|
    d = {
        "a": gi("1", 1, 10),
        "b": gi("1", 11, 20),
        "c": gi("1", 5, 15),
        "d": gi("1", 30, 40),
        "e": gi("2", 21, 30),
        "feature": gi("2", 1, 50),
    }
    d_plus = {x: d[x].get_stranded("+") for x in d}
    # d_minus = {x: d[x].get_stranded('-') for x in d}
    assert GI.merge([d_plus["a"], d_plus["a"]]) == d_plus["a"]
    assert GI.merge([d["a"], d["a"]]) == d["a"]
    assert GI.merge([d["a"], d["b"]]) == gi("1", 1, 20)
    assert GI.merge([d["a"], d["e"]]) is None  # chrom mismatch
    assert GI.merge([d["e"], d["feature"]]) == gi("2", 1, 50)  # containment
    assert GI.merge([d["a"], d_plus["a"]]) is None  # strand mismatch
    assert GI.merge([d_plus["a"], d_plus["a"]]) == d_plus["a"]
    assert GI.merge([d["a"], d["feature"]]) is None  # chr mismatch
    with pytest.raises(Exception) as e_info:
        d["a"].merge(
            d["feature"]
        )  # wrong usage, TODO: this still allows d['a'].merge( [d['feature']])


def test_loc_merge_unrestricted():
    d = {"a": gi("1", 1, 10), "b": gi(None, 11, 20)}
    assert GI.merge([d["a"], d["b"]]) == gi(None, 1, 20)
    assert GI.merge([d["b"], d["a"]]) == gi(None, 1, 20)


# def test_loc_merge_sorted():
#     a = {
#         'a': gi('1', 1, 10),
#         'c': gi('1', 5, 15),
#         'feature': gi('2', 1, 50),
#         'e': gi('2', 21, 30),
#     }
#     b = {
#         'a': gi('1', 1, 10),
#         'c': gi('3', 5, 15),
#         'feature': gi('4', 1, 50),
#         'e': gi('4', 21, 30)
#     }
#     for n,l in a.items():
#         l.data=n
#     for n,l in b.items():
#         l.data=n
#     for i in heapq.merge(a.values(), b.values()):
#         print(i, i.data)


def test_join():
    d = {
        "a": gi("1", 1, 10),
        "b": gi("1", 5, 15),
        "c": gi("1", 15, 20),
        "d": gi("1", 50, 100),
        "e": gi("3", 21, 30),
    }
    refdict = rna.RefDict({"1": None, "3": None})
    all = from_str("1:1-20, 1:50-100, 3:21-30")
    assert list(GI.join(list(d.values()), refdict=refdict)) == all
    assert (
        list(GI.join([d["a"], d["d"]], [d["b"], d["e"], d["c"]], refdict=refdict))
        == all
    )
    # see https://stackoverflow.com/questions/49071081/merging-overlapping-intervals-in-python
    intervals = from_str("1:3-9, 1:2-6, 1:8-10, 1:15-18")
    assert list(GI.join(intervals, refdict=refdict)) == from_str("1:2-10, 1:15-18")
    # see https://stackoverflow.com/questions/43600878/merging-overlapping-intervals
    intervals = from_str("1:1-3,1:4-10,1:5-12,1:6-8,1:20-33,1:30-35")
    assert list(GI.join(intervals, refdict=refdict)) == from_str("1:1-3,1:4-12,1:20-35")
    # join adjacent
    intervals = from_str("1:1-3,1:4-10,1:11-12")
    assert list(GI.join(intervals, refdict=refdict, join_adjacent=False)) == intervals
    assert list(GI.join(intervals, refdict=refdict, join_adjacent=True)) == from_str(
        "1:1-12"
    )


def test_distance():
    a = from_str("1:1-10,1:1-10,1:10-20,1:25-30,1:1-10,2:1-10,2:11-12")
    dist = [a.distance(b) for a, b in pairwise(a)]
    assert dist == [0, 0, 5, -15, None, 1]


def test_eq():
    a = from_str("1:1-10")
    assert a[0] in a
    assert a[0].copy() in a
    b = a[0].get_stranded("+")
    assert b not in a


def test_regexp():
    locs = "1:1-10(+),  1:1-10 (-), chr2:1-10, 1:30-40    (+),"
    assert (
        str(from_str(locs))
        == "[1:1-10 (+), 1:1-10 (-), chr2:1-10, 1:30-40 (+), :0-2147483647]"
    )


def test_dict():
    f = from_str(
        "1:1-10 (+),1:1-10 (-),1:10-20 (+),1:25-30 (-),1:1-10 (+),2:1-10,2:11-12"
    )
    d = {k: str(k) for k in f}
    assert all(k in d for k in f) and all(k in f for k in f)


def test_overlap():
    assert gi("1:1-10 (+)").overlap(gi("1:1-10 (+)")) == 10
    assert gi("1:1-10 (+)").overlap(gi("1:1-10 (-)")) == 10
    assert gi("1:1-10 (+)").overlap(gi("1:1-10 (-)"), strand_specific=True) == 0
    assert gi("1:1-10").overlap(gi("1:10-15")) == 1
    assert gi("1:5-10 (+)").overlap(gi("1:1-5 (-)"), strand_specific=True) == 0
    assert gi("1:5-10").overlap(gi("1:11-50")) == 0  # no overlap
    assert gi("1:5-10").overlap(gi("1:20-50")) == 0  # no overlap


def test_add_sub():
    d = {
        "a": gi("1:1-10"),
        "b": gi("1:20-30"),
        "c": gi("1:40-50"),
        "d": gi("1:2-9"),
        "e": gi("1:1-3"),
    }
    assert d['a'] + d['a'] == d['a']
    assert d['a'] + d['a'].get_stranded('+') == d['a']  # different strand, no overlap
    assert d['a'] + d['b'] == gi("1:1-30")
    assert sum([d['a'], d['b'], d['c']]) == gi("1:1-50")
    assert (d['a'] - d['a']).is_empty()
    assert (d['a'] - d['b']) == d['a']
    assert (d['a'] - d['d']) == [gi("1:1-1"), gi("1:10-10")]  # split
    assert (d['a'] - d['e']) == gi("1:4-10")
    assert (d['e'] - d['a']).is_empty()
    assert (d['a'] - (d['d'] + 1)) == gi("1:1-1")
    assert (d['a'] - (d['d'] - -1)) == gi("1:1-1")
    # create 100 sets of unstranded random intervals from 1 single chrom and test whether this is equal to the sum
    # note that merge is as fast as sum in this scenario.
    rints = rna.split_list(rna.random_intervals(chromosomes=['1'], n=10000), 100)
    for i in rints:
        assert sum(i) == GI.merge(i)


def test_sort():
    """Assert sort order including empty and unbounded intervals"""
    locs = from_str("1:1-10(+),3:5-100,1:1-10 (-), chr2:1-10,1:30-40(+)") + [
        gi(None, 200, 300),
        gi("1", end=10),
        gi("chr2", 2, 1),
    ]  # empty
    # sorted(locs) # no chrom order!
    refdict = rna.RefDict({"1": None, "chr2": None, "3": None}, name="test")
    assert sorted(locs, key=lambda x: (refdict.index(x.chromosome), x)), [
        locs[x] for x in [4, 5, 0, 2, 6, 3, 1]
    ]
    locs += [gi("chrX", 1, 10)]
    with pytest.raises(TypeError):
        print(GI.sort(locs, refdict=refdict))


def test_len():
    assert len(gi("chr1", 1, 2)) == 2  # interval
    assert len(gi("chr1", 1, 1)) == 1  # point
    assert (
        gi("chr1", 20, 10).is_empty() and len(gi("chr1", 20, 10)) == 0
    )  # empty interval
    assert len(gi()) == rna.MAX_INT  # None:-inf-inf # unbounded intervals
    assert len(gi("chr1", 1)) == rna.MAX_INT  # chr1:1-inf
    assert len(gi("chr1", None, 1)) == rna.MAX_INT  # chr1:-inf-1


def test_empty():
    assert gi("chr1", 1, 0).is_empty()
    assert not gi("chr1", 1, 0).overlaps(gi("chr1", 1, 0))
    assert gi("chr1", 1, 0).overlap(gi("chr1", 1, 0)) == 0
    assert gi("chr1", 1, 0) == gi(
        "chr1", 1000, 999
    )  # empty intervals are equal if on same chrom
    assert gi("chr1", 1, 0) != gi("chr2", 1000, 999)


def test_unbounded():
    assert gi().is_unbounded()


def test_updownstream():
    assert gi("chr1", 10, 20).get_upstream(3) is None  # no strand: return None
    assert [gi("chr1", 10, 20, "+").get_upstream(3)] == from_str("chr1:7-9(+)")
    assert [gi("chr1", 10, 20, "+").get_downstream(3)] == from_str("chr1:21-23(+)")
    assert [gi("chr1", 10, 20, "-").get_downstream(3)] == from_str("chr1:7-9(-)")
    assert [gi("chr1", 10, 20, "-").get_upstream(3)] == from_str("chr1:21-23(-)")


def test_toXXX():
    # HTSeq
    iv = gi("chr1", 1, 10)
    iv2 = HTSeq.GenomicInterval(
        iv.chromosome, iv.start - 1, iv.end, "." if iv.strand is None else iv.strand
    )
    assert iv.to_htseq() == iv2
    assert len(iv) == iv2.length
    # BED
    assert iv.to_bed(name="test") == "chr1\t0\t10\ttest"
    assert (
        iv.to_bed12(name="test", score=1000, rgb="1,2,3")
        == "chr1\t0\t10\ttest\t1000\t.\t0\t10\t1,2,3\t0\t10\t0"
    )
