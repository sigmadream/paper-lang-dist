from tests.integration.test_rtt_pipeline import RouteClient, SuccessEvaluator, _config, _problem
from rttdist.pipeline import run_pipeline_service


def test_pipeline_service_runs_one_route_per_problem_and_target_language(tmp_path):
    config = _config(tmp_path)
    problem = _problem(tmp_path)
    result = run_pipeline_service(config=config, run_id="svc", corpus_entries=(problem,), translation_client_factory=lambda: RouteClient(["target", "int main(){return 0;}"]), evaluate_source_fn=SuccessEvaluator())
    assert len(result) == 3
    assert [item.target_language for item in result] == ["c", "java", "python"]
