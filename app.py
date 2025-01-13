import streamlit as st
import pickle
import base64   #to insert the image of local device in background of streamlit app
with open('Student_Performance_estimator_model.pkl','rb') as model_file:
    student_performance_estimator=pickle.load(model_file)
#st.title("Student Performance Estimator")
# Function to encode image to base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Path to your image
img_path = "background image.webp"
img_base64 = get_base64_of_bin_file(img_path)
# Custom CSS to set the background image
st.markdown(
    f'''
    <style>
    html, body, [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{img_base64}");
        background-size: cover;
    }}
    </style>
    ''',
    unsafe_allow_html=True
    
)
st.title("Student Performance Estimator")
with st.form(key='form'):
    st.write("Please provide the following information to get prediction")
    hours_study=st.number_input("Hours you study in 24hours",key='hours',min_value=0,max_value=20)
    previous_score=st.number_input("Previous score out of 100",key='previous-score',min_value=0,max_value=100)
    extra_activities=st.selectbox("Participation in Extra-Curricular Activities",options=['No','Yes'])
    hours_sleep=st.number_input("Hours Sleep in day",key='sleep-hours',min_value=4,max_value=24-hours_study)
    Sample_papers_practiced=st.number_input("Sample Question Papers Practiced in day",key='sample-papers',min_value=0,max_value=100)
    if extra_activities=='No':
        extra_activities=0
    else:
        extra_activities=1
    submitted=st.form_submit_button("Submit Data")
    if submitted:
        no_of_inputs_submitted=0
        list_of_inputs=["hours_study","previous_score","extra_activities","hours_sleep","Sample_papers_practiced"]
        for each in list_of_inputs:
            if not each:
                st.error(f'Please provide the input for {each}')
                break
            else:
                no_of_inputs_submitted+=1
        if no_of_inputs_submitted==5:
            prediction=student_performance_estimator.predict([[hours_study,previous_score,extra_activities,hours_sleep,Sample_papers_practiced]])[0]
            st.success(f"Based on the data provided,the performance of student is {prediction:.2f}")
        
