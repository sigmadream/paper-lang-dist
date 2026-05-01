from tests.integration.test_rtt_pipeline import RouteClient, SuccessEvaluator, _config, _problem
from rttdist.pipeline import run_rtt_loop


def test_idempotent_completed_route_skips_translation(tmp_path):
    config = _config(tmp_path)
    problem = _problem(tmp_path)
    run_rtt_loop(config=config, run_id="idem", problem=problem, target_language="python", translation_client=RouteClient(["c", "java", "py", "int main(){return 0;}"]), evaluate_source_fn=SuccessEvaluator())
    result = run_rtt_loop(config=config, run_id="idem", problem=problem, target_language="python", translation_client=RouteClient([]), evaluate_source_fn=SuccessEvaluator())
    assert result.final_record.status.value == "success"
