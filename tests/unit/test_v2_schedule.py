from rttdist.experiment_v1 import execution_order


def test_each_problem_occupies_every_language_position_over_three_repeats():
    problems = tuple(f"p{i}" for i in range(40))
    targets = ("c", "java", "python")
    schedule = {"order": "balanced_seeded", "seed": 20260911}
    orders = [execution_order(problems, targets, schedule, repeat) for repeat in (1, 2, 3)]
    for order in orders:
        assert len(order) == len(set(order)) == 120
        assert set(order) == {(p, t) for p in problems for t in targets}
    for p in problems:
        sequences = [[t for problem, t in order if problem == p] for order in orders]
        for position in range(3):
            assert {sequence[position] for sequence in sequences} == set(targets)
    assert orders[0] == execution_order(problems, targets, schedule, 1)


def test_legacy_order_is_preserved():
    assert execution_order(("p1", "p2"), ("c", "java"), {}, None) == [
        ("p1", "c"), ("p1", "java"), ("p2", "c"), ("p2", "java")]
