from itertools import count
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

df_new=pd.read_csv (r'C:\Users\Jeevanandam\Desktop\HR Analytics\Home Appliancs Dashboard\Customer Overview Data.csv')
df_inv=pd.read_csv (r'C:\Users\Jeevanandam\Desktop\HR Analytics\Home Appliancs Dashboard\Customer Overview Data_csv1.csv')

st.markdown("<h2 style='text-align: center; color: black;'>Customers Segmentation</h2>", unsafe_allow_html=True)

option = st.selectbox(
     'Enter The Customer ID',
     df_inv['Cutom er ID'].to_list())
st.markdown("-----------------------------------------------------------------------")
st.markdown("")
st.markdown("")

sec1, sec2, sec3,sec4 = st.columns(4)
with sec1:
    pr=df_inv[df_inv["Cutom er ID"] == option]['first_name']
    for i in pr:
        st.subheader("Customer Name")
        st.subheader(i)
with sec2:
    pr=df_inv[df_inv["Cutom er ID"] == option]['email']
    for i in pr:
        st.subheader("Customer Email")
        st.subheader(i)
with sec4:
    pr=df_inv[df_inv["Cutom er ID"] == option]['Recency Category']
    for i in pr:
        st.subheader("Recent Purchase")
        st.subheader(i)
with sec3:
    pr=df_inv[df_inv["Cutom er ID"] == option]['DOB']
    for i in pr:
        st.subheader("Customer DOB")
        st.subheader(i)

st.markdown("")
st.markdown("")
st.markdown("-----------------------------------------------------------------------")

sec11, sec22, sec33,sec44 = st.columns(4)
with sec11:
    pr=df_inv[df_inv["Cutom er ID"] == option]['Dt_Customer']
    for i in pr:
        st.subheader("Last Purchase date")
        st.subheader(i)

with sec22:
    pr=df_inv[df_inv["Cutom er ID"] == option]['Product Name']
    for i in pr:
        st.subheader("Product Purchased")
        st.subheader(i)
with sec33:
    pr=df_inv[df_inv["Cutom er ID"] == option]['Sales']
    for i in pr:
        st.subheader("Purchase Amount")
        st.subheader(i)

with sec44:
    pr=df_inv[df_inv["Cutom er ID"] == option]['score']
    for i in pr:
        st.subheader("Purchase Score")
        st.subheader(i)



my_dict={'Age':[]}
my_dict1={'Age_cat':[]}

for i in df_new['Year_Birth']:
    my_dict['Age'].append(2022-df_new['Year_Birth'][i])
df_mon=pd.DataFrame.from_dict(my_dict)
df_new["Age"]=df_mon["Age"]

for i in df_new['Age']:
    if(i>0 and i<=30):
        my_dict1['Age_cat'].append("0-30")
    if(i>30 and i<=50):
        my_dict1['Age_cat'].append("30-50")   
    else:
        my_dict1['Age_cat'].append("50 Above") 
df_mon1=pd.DataFrame.from_dict(my_dict1)
df_new["Age_cat"]=df_mon1["Age_cat"]

my_dict2={'Income_cat':[]}

for i in df_new['Income']:
    if(i>0 and i<=50000):
        my_dict2['Income_cat'].append("0-50k")
    if(i>50000 and i<=100000):
        my_dict2['Income_cat'].append("50k-100k")   
    else:
        my_dict2['Income_cat'].append("100k Above")  

df_mon2=pd.DataFrame.from_dict(my_dict2)
df_new["Income_cat"]=df_mon2["Income_cat"]

my_dict3={'Recency_cat':[]}

for i in df_new['Recency']:
    if(i>0 and i<=30):
        my_dict3['Recency_cat'].append("0-30 days")
    if(i>30 and i<=60):
        my_dict3['Recency_cat'].append("30-60 days")   
    if(i>60 and i<=90):
        my_dict3['Recency_cat'].append("60-90 days")  
    else:
        my_dict3['Recency_cat'].append("Above 90 days")  

df_mon3=pd.DataFrame.from_dict(my_dict3)
df_new["Recency_cat"]=df_mon3["Recency_cat"]

st.markdown("")
st.markdown("")

nc=df_new['ID'].count()
st.markdown("")
st.markdown("")
st.markdown("-----------------------------------------------------------------------")

col11, col22, col33= st.columns(3)


with col11:
    st.markdown("<h3 style='text-align: center; color: black;'>Customers By Education</h3>", unsafe_allow_html=True)

    basic=0
    master=0
    n_cycle=0
    phd=0
    gra=0
    for i in range(0,len(df_new['Age'])):
        if(df_new["Education"][i]=="Basic"):
            basic=basic+1
        if(df_new["Education"][i]=="Master"):
            master=master+1
        if(df_new["Education"][i]=="2n Cycle"):
            n_cycle=n_cycle + 1
        if(df_new["Education"][i]=="PhD"):
            phd=phd+1
        else:
            gra=gra+1

    labels = ['Basic','Master','2n_Cycle','PhD','Graduation']
    values = [basic,master,n_cycle,phd,gra]
    df3 = px.data.iris()

    fig1 = px.bar(df3, x=labels, y=values, orientation='v')
    fig1.update_layout(
        xaxis_title="Count of Customers",
        yaxis_title="Education")
    st.plotly_chart(fig1)

with col22:
    st.markdown("<h3 style='text-align: center; color: black;'>Customers By Kid_Flag</h3>", unsafe_allow_html=True)

    Single=0
    Together=0
    Married=0
    Divorced=0
    Alone=0
    Absured=0
    Widow=0
    YOLO=0
    for i in range(0,len(df_new['Age'])):
        if(df_new["Marital_Status"][i]=="Single"):
            Single=Single+1
        if(df_new["Marital_Status"][i]=="Together"):
            Together=Together+1
        if(df_new["Marital_Status"][i]=="Married"):
            Married=Married + 1
        if(df_new["Marital_Status"][i]=="Divorced"):
            Divorced=Divorced+1
        if(df_new["Marital_Status"][i]=="Alone"):
            Alone=Alone+1
        if(df_new["Marital_Status"][i]=="Absured"):
            Absured=Absured+1
        if(df_new["Marital_Status"][i]=="Widow"):
            Widow=Widow+1
        else:
            YOLO=YOLO+1
    labels = ['Single','Together','Married','Divorced','Alone','Absured','Widow','YOLO']
    values = [Single,Together,Married,Divorced,Alone,Absured,Widow,YOLO]
    df3 = px.data.iris()
    fig1 = px.bar(df3, x=values, y=labels, orientation='h')
    fig1.update_layout(
        xaxis_title="Count of Customers",
        yaxis_title="Marital Status")
    st.plotly_chart(fig1)   

with col33:
    st.markdown("<h3 style='text-align: center; color: black;'>Customers By Teen_Flag</h3>", unsafe_allow_html=True)

    yes=0
    no=0
    for i in range(0,len(df_new['Age'])):
        if(df_new["Teenhome"][i]==1):
            yes=yes+1
        if(df_new["Teenhome"][i]==0):
            no=no+1 
    labels = ['Has Teen','Has No Teen']
    values = [yes,no]

# Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])   
    st.plotly_chart(fig)  
st.markdown("----------------------------------------------")

col111, col222, col333= st.columns(3)
with col111:
    st.markdown("<h3 style='text-align: center; color: black;'>Customers By Purchase Recency and Age</h3>", unsafe_allow_html=True)

    df_new1=df_new.drop(['Year_Birth','Education','Marital_Status','Income','Kidhome','Teenhome','Dt_Customer','Age','Income_cat','Recency'],axis=1)
    df_new1=df_new1.groupby(['Recency_cat','Age_cat'],as_index=False)['ID'].count()
    df3 = px.data.iris()

    fig = px.bar(df3, y=df_new1['Recency_cat'].to_list(), x=df_new1["ID"].to_list(),
    color=df_new1['Age_cat'], barmode = 'group',orientation='h')
    fig.update_layout(
        xaxis_title="Count of Customers",
        yaxis_title="Recency")
    st.plotly_chart(fig)  

with col222:
    st.markdown("<h3 style='text-align: center; color: black;'>Customers By Income and Age</h3>", unsafe_allow_html=True)

    df_new1=df_new.drop(['Year_Birth','Education','Marital_Status','Income','Kidhome','Teenhome','Dt_Customer','Age','Recency_cat','Recency'],axis=1)
    df_new1=df_new1.groupby(['Income_cat','Age_cat'],as_index=False)['ID'].count()
    df3 = px.data.iris()

    fig = px.bar(df3, x=df_new1['Income_cat'].to_list(), y=df_new1["ID"].to_list(),
    color=df_new1['Age_cat'], barmode = 'group')
    fig.update_layout(
        xaxis_title="Count of Customers",
        yaxis_title="Income Category")
    st.plotly_chart(fig)  
with col333:
    st.markdown("<h3 style='text-align: center; color: black;'>Customers By Age and Age Category</h3>", unsafe_allow_html=True)

    df_new1=df_new.drop(['Year_Birth','Education','Marital_Status','Income','Kidhome','Teenhome','Dt_Customer','Income_cat','Recency_cat','Recency'],axis=1)
    df_new1=df_new1.groupby(['Age','Age_cat'],as_index=False)['ID'].count()
    df3 = px.data.iris()

    fig = px.bar(df3, x=df_new1['Age'].to_list(), y=df_new1["ID"].to_list(),
    color=df_new1['Age_cat'], barmode = 'group')
    fig.update_layout(
        xaxis_title="Age",
        yaxis_title="Count of Customers")
    st.plotly_chart(fig)  

st.markdown("----------------------------------------------")

