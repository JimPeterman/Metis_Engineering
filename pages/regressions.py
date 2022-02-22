import pickleimport streamlit as stfrom ref_calcs import friend_percentiledef app():     ###### Create a CRF percentile calculator.        st.write('''    ## Determine Your Fitness Percentile        Below you can determine your fitness percentile if you already know \    your VO2max or you can estimate your VO2max to estimate your fitness \    percentile.        (Reference values for fitness percentiles are based on US-only data and     come from      [this 2022 FRIEND publication](https://www.mayoclinicproceedings.org/article/S0025-6196(21)00645-5/fulltext))    ''')        crf_type = st.radio("Do you already know your VO2max?", ("Yes", "No"),                         index=1)        if crf_type == "Yes":        col1, col2 = st.columns(2)                with col1:            sex = st.radio("Your sex:", ("Male", "Female"), index=1)            mode = st.radio("Testing mode you used:",                                 ("Treadmill", "Cycle Ergometer"), index=0)                with col2:            age = st.selectbox("Your age range:", ("20-29", "30-39", "40-49",                                                   "50-59", "60-69", "70-79",                                                    "80-89"), index=1)            age = int(age[:2])            vo_2 = st.number_input('Enter your VO2max value:', min_value=(0.0),                                max_value=(99.9), step=0.1, value=38.6)                # Print the CRF results.        crf_perc = friend_percentile(vo_2, age, sex, mode)        crf_text = f"Your fitness percentile is: {crf_perc}%"                # Determine color to print results.        if crf_perc <= 33.3:            prt_color = "Red"        elif crf_perc >= 66.6:            prt_color = "Green"        else:             prt_color = "Black"                    crf_result = f"<p style='color:{prt_color}; font-size: 24px;'>{crf_text}</p>"        st.markdown(crf_result, unsafe_allow_html=True)        # st.write(f"#### Your fitness percentile is: {crf_perc}%")                             else:        st.info("""                 This estimated VO2max comes from real-time regression                  analysis on FRIEND.""")                # The list of countries available based on analysis (>500 tests).        lst_countries = open("./data/reg_model_country_lst.txt", "r").read()        lst_countries = lst_countries.split("\n")        # with open('./data/reg_model_country_lst.pickle','rb') as read_file:        #         lst_countries = pickle.load(read_file)        lst_countries = ["Global"] + lst_countries                col1, col2 = st.columns(2)                with col1:            sex = st.radio("Your sex:", ("Male", "Female"), index=1)            sex_num = 1 if sex == "Male" else 0            ht = st.selectbox("Select your height:",                               ("5 ft, 0 in", "5ft, 1 in",                               "5 ft, 2 in", "5ft, 3 in",                               "5 ft, 4 in", "5ft, 5 in",                               "5 ft, 6 in", "5ft, 7 in",                               "5 ft, 8 in", "5ft, 9 in",                               "5 ft, 10 in", "5ft, 11 in",                               "6 ft, 0 in", "6ft, 1 in",                               "6 ft, 2 in", "6ft, 3 in",                               "6 ft, 4 in", "6ft, 5 in",                               "6 ft, 6 in", "6ft, 7 in",                               "6 ft, 8 in", "6ft, 9 in",                               "6 ft, 10 in", "6ft, 11 in"), index=7)            ht = (int(ht.split(", ")[0][0]) * 12) + (int(ht.split(", ")[1][:2]))            mode = st.radio("What exercise mode are you interested in",                            ("Treadmill", "Cycling"), index=0)            mode_num = 1 if mode == "Treadmill" else 0                with col2:            age = st.number_input("Enter your age:", min_value=(18),                                   max_value=(90), step=1, value=(29))            wt = st.slider("Select your weight (in lbs):", min_value=(40),                           max_value=(350), value=(170), step=(1))            country = st.selectbox("Select a Region/Country:",                                lst_countries, index=0)                           # Import the model depending on which data user wants.        # Then, create the appropriate list of variables to enter into model.        if country == "Global":            with open('./data/reg_model_global.pickle','rb') as read_file:                lm_OLS = pickle.load(read_file)            entry_for_model = [age, sex_num, ht, wt, mode_num]                else:                          with open('./data/reg_model_country.pickle','rb') as read_file:                lm_OLS = pickle.load(read_file)            # 1 for country selected (skipping first entry of lst ("Global"))            entry_for_model = [1 if x == country else 0 for x in lst_countries[1:]]            entry_for_model = [age, sex_num, ht, wt, mode_num] + entry_for_model            # Enter everything into the regression for calculations.            vo_2 = round(lm_OLS.predict([entry_for_model])[0],1)        crf_perc = friend_percentile(vo_2, age, sex, mode)                st.write(f"#### Your estimated fitness is: {vo_2} ml/kg/min")        # Print the CRF results.        crf_perc = friend_percentile(vo_2, age, sex, mode)        crf_text = f"Your estimated fitness percentile is: {crf_perc}%"                # Determine color to print results.        if crf_perc <= 33:            prt_color = "Red"        elif crf_perc >= 67:            prt_color = "Green"        else:             prt_color = "Black"                    crf_result = f"<p style='color:{prt_color}; font-size: 24px;'>{crf_text}</p>"        st.markdown(crf_result, unsafe_allow_html=True)        st.write("_**As highlighted in [this study](https://www.jacc.org/doi/abs/10.1016/j.jacc.2018.08.2166),\                 fitness percentiles <33% are associated with increased \                 mortality risk compared to moderate and high (>67%) fitness._")    if crf_type == "No":        metrics = st.radio("Would you like to view the metrics related to \                           the model used to predict this VO2max?",                           ("Yes", "No"), index = 1)                                   if metrics == "Yes":            if country == "Global":                st.write("Performance metrics for the global prediction model.")                                with open('./data/reg_model_global_metrics.pickle','rb') as read_file:                    dct_model_metrics = pickle.load(read_file)                with open('./data/reg_model_global_graph.pickle','rb') as read_file:                    fig_reg = pickle.load(read_file)                with open('./data/reg_model_global_ba.pickle','rb') as read_file:                    fig_ba = pickle.load(read_file)            else:                   st.write("Performance metrics for the prediction model \                         that includes country as a feature.")                with open('./data/reg_model_country_metrics.pickle','rb') as read_file:                    dct_model_metrics = pickle.load(read_file)                with open('./data/reg_model_country_graph.pickle','rb') as read_file:                    fig_reg = pickle.load(read_file)                with open('./data/reg_model_country_ba.pickle','rb') as read_file:                    fig_ba = pickle.load(read_file)                                col1_, col2_ = st.columns(2)            with col1_:                st.metric("The R2 on the test data is: ",                           dct_model_metrics["Test"]["R2"])                st.metric("The RMSE on the test data is: ",                           dct_model_metrics["Test"]["R2"])                st.metric("The MAE on the test data is: ",                           dct_model_metrics["Test"]["R2"])            with col2_:                st.pyplot(fig_reg)                st.pyplot(fig_ba)