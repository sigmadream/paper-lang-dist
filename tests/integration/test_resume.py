from tests.integration.test_rtt_pipeline import RouteClient, SuccessEvaluator, _config, _problem
from rttdist.pipeline import run_rtt_loop


def test_completed_route_rerun_reuses_final_manifest(tmp_path):
    config = _config(tmp_path)
    problem = _problem(tmp_path)
    first = run_rtt_loop(config=config, run_id="resume", problem=problem, target_language="python", translation_client=RouteClient(["c", "java", "py", "int main(){return 0;}"]), evaluate_source_fn=SuccessEvaluator())
    second = run_rtt_loop(config=config, run_id="resume", problem=problem, target_language="python", translation_client=RouteClient([]), evaluate_source_fn=SuccessEvaluator())
    assert first.final_record.status == second.final_record.status
    assert second.iteration_count == 1
