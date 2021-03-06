from app.calculation_service.model.scenario_inputs import ScenarioInputs
from app.calculation_service.model.study_design import StudyDesign
from app.calculation_service.api import _generate_models, _calculate_power
import pandas as pd

pd.set_option('precision', 7)


def json_power(json_path):
    with open(json_path, 'r') as f:
        data = f.read()
    inputs = ScenarioInputs().load_from_json(data)
    scenario = StudyDesign().load_from_json(data)
    models = _generate_models(scenario, inputs)
    results = []
    for m in models:
        result = _calculate_power(m)
        outdata = {'Power': result['power'],
                   'Test': result['test'],
                   'Sigma Scale': result['model']['variance_scale_factor'],
                   'Beta Scale': result['model']['means_scale_factor'],
                   'Total N': result['model']['total_n'],
                   'Alpha': result['model']['alpha']}
        results.append(outdata)

    return pd.DataFrame(results)


def tex_table(file_path, V3_JSON, V2_results):
    _df_vtest = json_power(file_path + V3_JSON)

    _df_v2results = pd.read_csv(file_path + V2_results)

    _df_output = pd.merge(_df_vtest, _df_v2results, how='outer',
                          left_on=['Sigma Scale', 'Beta Scale', 'Total N', 'Alpha'],
                          right_on=['Sigma Scale', 'Beta Scale', 'Total N', 'Alpha'])
    _df_output['deviation_sas_v3'] = abs(_df_output.Power - _df_output.SAS_Power).apply(lambda x: '%.7f' % x)
    _df_output['deviation_sim_v3'] = abs(_df_output.Power - _df_output.Sim_Power).apply(lambda x: '%.7f' % x)
    _df_output = _df_output.sort_values(by=['Sigma Scale', 'Beta Scale', 'Total N', 'Alpha'])
    _df_output = _df_output.round(
        {'Power': 7, 'SAS_Power': 7, 'deviation_sas_v3': 7, 'Sim_Power': 7, 'deviation_sim_v3': 7})
    _df_output.Power = _df_output.Power.apply('{:0<9}'.format)
    _df_output.SAS_Power = _df_output.SAS_Power.apply('{:0<9}'.format)
    _df_output.deviation_sas_v3 = _df_output.deviation_sas_v3.apply('{:0<9}'.format)
    _df_output.Sim_Power = _df_output.Sim_Power.apply('{:0<9}'.format)
    _df_output.deviation_sim_v3 = _df_output.deviation_sim_v3.apply('{:0<9}'.format)
    _df_output["SAS Power (deviation)"] = _df_output["SAS_Power"].astype('str') + " (" + _df_output[
        "deviation_sas_v3"].astype('str') + ")"
    _df_output["Sim Power (deviation)"] = _df_output["Sim_Power"].astype('str') + " (" + _df_output[
        "deviation_sim_v3"].astype('str') + ")"
    _df_print = _df_output[
        ['Power', 'SAS Power (deviation)', 'Sim Power (deviation)', 'Test_x', 'Sigma Scale', 'Beta Scale', 'Total N',
         'Alpha']]
    return _df_print.to_latex(index=False)


file_path = r'C:\Users\liqian\Dropbox (UFL)\Project_QL\2017_GLIMMPSE_V3\PyGLIMMPSE\TEXT\\'

test2 = tex_table(file_path, 'Test02_V3_ConditionalPairedTTest.json', 'Test02_V3_ConditionalPairedTTest_v2results.csv')
test3 = tex_table(file_path, 'Test03_V3_ConditionalTwoSampleTTest3DPlot.json', 'Test03_V3_ConditionalTwoSampleTTest3DPlot_v2results.csv')

print(test3)