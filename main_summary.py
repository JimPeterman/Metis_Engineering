# # Create/update the SQL database with the FRIEND data.# import sql_db_creation# sql_db_creationfrom analysis import summary_test_count, line_graph_summaries, \    regression_creation, publication_scraper# # Create/update the list of publications.# import publication_scraper# publication_scraper# Update the summary tables for the US/Global maps of test numbers.summary_test_count# Update the tables for the line graphs of VO2 and other metrics.line_graph_summaries# Perform the regression analysis to build VO2max predictino model.regression_creation