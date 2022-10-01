import pm4py
import pandas as pd
from pm4py.objects.conversion.log import converter as log_conv_fact
from pm4py.algo.filtering.log.timestamp import timestamp_filter
from pm4py.algo.filtering.log.attributes import attributes_filter
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.visualization.petri_net import visualizer as pn_vis
from pm4py.evaluation import evaluator as evaluation_factory
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay

log = pm4py.read_xes("BPI Challenge 2017.xes")  # READS THE EVENT LOG
event_stream_log = log_conv_fact.apply(log,
                                       variant=log_conv_fact.TO_EVENT_STREAM)  # CONVERTS THE EVENT LOG TO EVENT STREAM
filtered_log = timestamp_filter.filter_traces_contained(log, "2016-01-01 00:00:00",
                                                        "2016-01-20 23:59:59")  # it creates a filtered log for the dates through 1-20 of january
activities = attributes_filter.get_attribute_values(log, "concept:name")

print("Trace Attributes: ", list(log[0].attributes.keys()))  # prints trace attributes
print("Event Attributes: ", list(log[0][0].keys()))  # prints event attributes
print("Number of traces: ", len(log))  # prints number of traces
print("Number of events: ", len(event_stream_log))  # prints number of events
print("Τhe diferrent events of the log are: ", activities)  # prints the different events and how many times appeared in the event log

# --------------ERWTHMA 6 - ORIGINAL  EVENT LOG

# ALPHA MINER
net_a, initial_marking_a, final_marking_a = alpha_miner.apply(log)

gviz = pn_vis.apply(net_a, initial_marking_a, final_marking_a)
pn_vis.save(gviz, "alphaminer.jpg")
pn_vis.view(gviz)
# INDUCTIVE MINER
net_in, initial_marking_in, final_marking_in = inductive_miner.apply(log)

gviz1 = pn_vis.apply(net_in, initial_marking_in, final_marking_in)
pn_vis.save(gviz1, "inductive.jpg")
pn_vis.view(gviz1)
# HEURISTICS MINER
net_he, initial_marking_he, final_marking_he = heuristics_miner.apply(log, parameters={
    heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.99})
gviz2 = pn_vis.apply(net_he, initial_marking_he, final_marking_he)
pn_vis.save(gviz2, "heuristics.jpg")
pn_vis.view(gviz2)

# ERWTHMA 7- ORIGINAL EVENT LOG
alpha_eval_result = evaluation_factory.apply(log, net_a, initial_marking_a, final_marking_a)
alpha_miner_eval_result = pd.DataFrame(alpha_eval_result)  # converts output to dataframe
print('Evaluation result of Alpha Miner: ', alpha_miner_eval_result)

inductive_eval_result = evaluation_factory.apply(log, net_in, initial_marking_in, final_marking_in)
inductive_miner_eval_result = pd.DataFrame(inductive_eval_result)  # converts output to dataframe
print("Evaluation result of Inductive miner: ", inductive_miner_eval_result)

heuristics_eval_result = evaluation_factory.apply(log, net_he, initial_marking_he, final_marking_he)
heuristics_miner_eval_result = pd.DataFrame(heuristics_eval_result)  # converts output to dataframe
print("Evaluation result of heuristics miner: ", heuristics_miner_eval_result)

# ERWTHMA 8 - ORIGINAL EVENT LOG
replayed_traces_alpha = token_replay.apply(log, net_a, initial_marking_a, final_marking_a)  # replay fitness alpha miner
rep_tra_alpha_df = pd.DataFrame(replayed_traces_alpha)  # converts conformance replay output to dataframe

replayed_traces_ind = token_replay.apply(log, net_in, initial_marking_in,
                                         final_marking_in)  # replay fit inductive miner
rep_tra_ind_df = pd.DataFrame(replayed_traces_ind)  # converts conformance replay output to dataframe

replayed_traces_heu = token_replay.apply(log, net_he, initial_marking_he,
                                         final_marking_he)  # replay fit heuristics miner
rep_tra_heu_df = pd.DataFrame(replayed_traces_heu)  # converts conformance replay output to dataframe

# each variable counts the values of FALSE-TRUE in column trace_is_fit of the output dataframe
# then they are transformed into dataframes in order to be stored in an excel spreadsheet
trace_fitness_alpha = rep_tra_alpha_df.trace_is_fit.value_counts()
trace_fitness_ind = rep_tra_ind_df.trace_is_fit.value_counts()
trace_fitness_heu = rep_tra_heu_df.trace_is_fit.value_counts()
trace_fitness_alpha_df = pd.DataFrame(trace_fitness_alpha)
trace_fitness_ind_df = pd.DataFrame(trace_fitness_ind)
trace_fitness_heu_df = pd.DataFrame(trace_fitness_heu)
print(rep_tra_alpha_df)
print(rep_tra_ind_df)
print(rep_tra_heu_df)
print("How many traces fit in alpha miner: \n", trace_fitness_alpha_df)
print("How many traces fit in inductive miner: \n", trace_fitness_ind_df)
print("How many traces fit in heuristics miner: \n", trace_fitness_heu_df)

xlwriter = pd.ExcelWriter("business process mining results.xlsx")
alpha_miner_eval_result.to_excel(xlwriter, sheet_name='results', startrow=0, startcol=0)
inductive_miner_eval_result.to_excel(xlwriter, sheet_name='results', startrow=9, startcol=0)
heuristics_miner_eval_result.to_excel(xlwriter, sheet_name='results', startrow=18, startcol=0)
trace_fitness_alpha_df.to_excel(xlwriter, sheet_name='results', startrow=27, startcol=0)
trace_fitness_ind_df.to_excel(xlwriter, sheet_name='results', startrow=30, startcol=0)
trace_fitness_heu_df.to_excel(xlwriter, sheet_name='results', startrow=33, startcol=0)
xlwriter.close()

# -------- FILTERED EVENT LOG DATES BETWEEN 1-20 JANUARY

# ALPHA MINER
net_a_f, initial_marking_a_f, final_marking_a_f = alpha_miner.apply(filtered_log)

gviz_f = pn_vis.apply(net_a_f, initial_marking_a_f, final_marking_a_f)
pn_vis.save(gviz_f, "alphaminer_filtered_log.jpg")
pn_vis.view(gviz_f)
# INDUCTIVE MINER
net_in_f, initial_marking_in_f, final_marking_in_f = inductive_miner.apply(filtered_log)

gviz_f1 = pn_vis.apply(net_in_f, initial_marking_in_f, final_marking_in_f)
pn_vis.save(gviz_f1, "inductive_filtered_log.jpg")
pn_vis.view(gviz_f1)

# HEURISTICS MINER
net_he_f, initial_marking_he_f, final_marking_he_f = heuristics_miner.apply(filtered_log, parameters={
    heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.99})
gviz_f2 = pn_vis.apply(net_he_f, initial_marking_he_f, final_marking_he_f)
pn_vis.save(gviz_f2, "heuristics_filtered_log.jpg")
pn_vis.view(gviz_f2)

# FILTERED EVENT LOG

alpha_eval_result_f = evaluation_factory.apply(filtered_log, net_a_f, initial_marking_a_f, final_marking_a_f)
alpha_eval_result_fdf = pd.DataFrame(alpha_eval_result_f)  # converts output to dataframe
print('Evaluation result of Alpha Miner: ', alpha_eval_result_f)

inductive_eval_result_f = evaluation_factory.apply(filtered_log, net_in_f, initial_marking_in_f, final_marking_in_f)
inductive_eval_result_fdf2 = pd.DataFrame(inductive_eval_result_f)  # converts output to dataframe
print("Evaluation result of Inductive miner: ", inductive_eval_result_f)

heuristics_eval_result_f = evaluation_factory.apply(filtered_log, net_he_f, initial_marking_he_f, final_marking_he_f)
heuristics_eval_result_fdf3 = pd.DataFrame(heuristics_eval_result_f)  # converts output to dataframe
print("Evaluation result of heuristics miner: ", heuristics_eval_result_f)

##FILTERED EVENT LOG
replayed_traces_alpha_f = token_replay.apply(filtered_log, net_a_f, initial_marking_a_f,
                                             final_marking_a_f)  # replay fitness alpha miner
rep_tra_alpha_fdf = pd.DataFrame(replayed_traces_alpha_f)  # converts conformance replay output to dataframe

replayed_traces_ind_f = token_replay.apply(filtered_log, net_in_f, initial_marking_in_f,
                                           final_marking_in_f)  # replay fit inductive miner

rep_tra_ind_fdf = pd.DataFrame(replayed_traces_ind_f)  # converts conformance replay output to dataframe

replayed_traces_heu_f = token_replay.apply(filtered_log, net_he_f, initial_marking_he_f,
                                           final_marking_he_f)  # replay fit heuristics miner
rep_tra_heu_fdf = pd.DataFrame(replayed_traces_heu_f)  # converts conformance replay output to dataframe

# each variable counts the values of FALSE-TRUE in column trace_is_fit of the output dataframe
# then they are transformed into dataframes in order to be stored in an excel spreadsheet
trace_fitness_alpha_f = rep_tra_alpha_fdf.trace_is_fit.value_counts()
trace_fitness_ind_f = rep_tra_ind_fdf.trace_is_fit.value_counts()
trace_fitness_heu_f = rep_tra_heu_fdf.trace_is_fit.value_counts()
trace_fitness_alpha_fdf = pd.DataFrame(trace_fitness_alpha_f)
trace_fitness_ind_fdf2 = pd.DataFrame(trace_fitness_ind_f)
trace_fitness_heu_fdf3 = pd.DataFrame(trace_fitness_heu_f)
print(rep_tra_alpha_fdf)
print(rep_tra_ind_fdf)
print(rep_tra_heu_fdf)
print("How many traces fit in alpha miner: \n", trace_fitness_alpha_fdf)
print("How many traces fit in inductive miner: \n", trace_fitness_ind_fdf2)
print("How many traces fit in heuristics miner: \n", trace_fitness_heu_fdf3)

# the code below saves all the dataframes into an excel file in one sheet
xlwriter = pd.ExcelWriter("business process mining filtered log results.xlsx")
alpha_eval_result_fdf.to_excel(xlwriter, sheet_name='results of filtered log', startrow=0, startcol=0)
inductive_eval_result_fdf2.to_excel(xlwriter, sheet_name='results of filtered log', startrow=9, startcol=0)
heuristics_eval_result_fdf3.to_excel(xlwriter, sheet_name='results of filtered log', startrow=18, startcol=0)
trace_fitness_alpha_fdf.to_excel(xlwriter, sheet_name='results of filtered log', startrow=27, startcol=0)
trace_fitness_ind_fdf2.to_excel(xlwriter, sheet_name='results of filtered log', startrow=30, startcol=0)
trace_fitness_heu_fdf3.to_excel(xlwriter, sheet_name='results of filtered log', startrow=33, startcol=0)
xlwriter.close()

