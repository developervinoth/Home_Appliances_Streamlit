from turtle import width
import streamlit as st
import pandas as pd

from datetime import datetime, timedelta
from dateutil.relativedelta import *

import calendar

from sorted_months_weekdays import *

from sort_dataframeby_monthorweek import *
import plotly.graph_objects as go
import plotly.express as px
from itertools import count

# loading DataFrame


st.set_page_config(layout="wide")

@st.cache(allow_output_mutation=True)
def cache_data():
    transactionsDf = pd.read_excel('assets/data/TransactionsDim.xlsx')
    InventoryDf=pd.read_csv ('assets/data/inventory_new.csv')
    visitorsDf  = pd.read_excel('assets/data/visitors_dim.xlsx')
    df_revenue = pd.read_csv('assets/data/Drevenue_csv.csv')
    df_product = pd.read_csv('assets/data/Dproduct_csv.csv')
    df_expense = pd.read_csv('assets/data/Expenses_csv.csv')
    df_Account = pd.read_csv('assets/data/dAccount_csv.csv')
    df_new = pd.read_csv('assets/data/CustomerOverView.csv')
    df_inv = pd.read_csv('assets/data/CustomerOverView1.csv')
    return transactionsDf, InventoryDf, visitorsDf, df_revenue, df_product, df_expense, df_Account, df_new, df_inv

transactionsDf, InventoryDf, visitorsDf, df_revenue, df_product, df_expense, df_Account, df_new, df_inv = cache_data()

st.sidebar.header('Home Appliances Dashboard')
st.markdown("")
st.markdown("")
sideBarSelection = st.sidebar.selectbox(options=['EMI Simulator','Customer Segmentation' ,'Foot Traffic vs Digital Traffic', 'Inventory Control', 'Financial Simulator'], label='Select Page')

print(sideBarSelection)


# EMI Simulator
if sideBarSelection == 'EMI Simulator':

    st.header('EMI Simulator')

    col1, col2, col3 = st.columns(3)

    with col1:
        p = st.number_input('Principa   l Amount', step=100)

    with col2:
        R = st.number_input('Annual Interest in %', step=1)

    with col3:
        n = st.number_input('Number of Months', step=1)

    r = R/(12*100)

    if p and R and n is not 0:

        # Calculating interest rate per month
        r = R / (12 * 100)

        # Calculating Equated Monthly Installment (EMI)
        emi = p * r * ((1 + r) ** n) / ((1 + r) ** n - 1)
        print(emi)
        resultEmi = round(emi)
        interestPayable = round((emi * n) - p)
        totalPayment = round(emi*n)
    else:
        resultEmi = 0
        interestPayable = 0
        totalPayment = 0

    with col1:
        st.text('EMI ')
        st.subheader(str(resultEmi))

    with col2:
        st.text('Total Interest Payable')
        st.subheader(str(interestPayable))

    with col3:
        st.text('Total Payment')
        st.subheader(str(totalPayment))

    todayDate = datetime.now()

    endDate = todayDate + relativedelta(months=+n)

    dateRange = pd.date_range(todayDate.date(), endDate.date())

    emiDf = pd.DataFrame()
    emiDf['Date'] = pd.DataFrame(dateRange)

    emiDf['yearOfDate'] = emiDf['Date'].apply(lambda date: date.year)

    emiDf['monthOfDate'] = emiDf['Date'].apply(lambda date: date.month)

    monthWiseEmi = {}
    tempEmi = 0

    for i in range(1, n+1):
        tempEmi = tempEmi + emi
        monthWiseEmi[i] = round(tempEmi)

    emiDf_grouped = emiDf.groupby(by=['yearOfDate', 'monthOfDate']).count()

    emiDf_grouped.drop(emiDf_grouped.tail(1).index, inplace=True)

    emiDf_grouped['monthWiseEmi'] = monthWiseEmi.values()

    emiDf_grouped.reset_index(inplace=True)

    st.subheader('EMI Repayment Schedule')
  
    emiDf_grouped['Month'] = emiDf_grouped['monthOfDate'].apply(lambda value: calendar.month_name[value])


    emiDf_grouped.rename(columns={'yearOfDate': 'Year', 'monthWiseEmi': 'Loan Paid to Date'}, inplace=True)
    print(emiDf_grouped)
    st.table(emiDf_grouped[['Year','Month','Loan Paid to Date']])


elif sideBarSelection == 'Foot Traffic vs Digital Traffic':
    st.title('Foot Traffic vs Digital Traffic')
    # To Calculate total Transaction Count

    col1, col2, col3,col4 = st.columns(4)
    # st.write('Total Transactions Count')
    with col1:
        totalTransactionCount  = transactionsDf['transactionId'].count()
    # st.header(totalTransactionCount)

        st.markdown("<h5 style='text-align: center;'>Total Transactions Count</h5>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; '>"+str(totalTransactionCount)+"</h2>", unsafe_allow_html=True)
    
    with col2:
        footTraffic = len(visitorsDf[visitorsDf['modeOfVisit'] == 'Store'])
        st.markdown("<h5 style='text-align: center;'>Foot Traffic</h5>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; '>"+str(footTraffic)+"</h2>", unsafe_allow_html=True)

    with col3:
        digitalTraffic = len(visitorsDf[visitorsDf['modeOfVisit'] == 'Online'])
        st.markdown("<h5 style='text-align: center;'>Digital Traffic</h5>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; '>"+str(digitalTraffic)+"</h2>", unsafe_allow_html=True)

    with col4:

        uniqueCustomers = transactionsDf.groupby('customerId').count().reset_index()['customerId'].count()
        st.markdown("<h5 style='text-align: center;'>Overall Conversion Rate</h5>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; '>"+str(round(uniqueCustomers/(len(visitorsDf)) * 100, 2))+"%</h2>", unsafe_allow_html=True)
        


    lineGraph = pd.DataFrame(transactionsDf.groupby('month').count()['transactionId']).reset_index()
    lineGraph = Sort_Dataframeby_Month(df=lineGraph,monthcolumnname='month')
    fig = go.Figure()
    fig = px.line(lineGraph, x="month", y="transactionId", labels = {'month': 'Month', 'transactionId': 'Transactions'}, title="Month wise Total Transactions")
    fig.update_layout(
            height = 300,)
    st.plotly_chart(fig, use_container_width = True)

    col1, col2 = st.columns(2)

    with col1:
        # To Calculate Transaction count of Store Visitors
        # st.write('Transactions Count on Store')
        storeTransactionCount  = transactionsDf[transactionsDf['modeOfVisit'] == 'Store']['transactionId'].count()
        # st.header(storeTransactionCount)

        st.markdown("<h5 style='text-align: center;'>Transactions Count on Store</h5>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; '>"+str(storeTransactionCount)+"</h2>", unsafe_allow_html=True)
        

        lineGraph = pd.DataFrame(transactionsDf[transactionsDf['modeOfVisit']=='Store'].groupby('month').count()['transactionId']).reset_index()
        lineGraph = Sort_Dataframeby_Month(df=lineGraph,monthcolumnname='month')
        fig = go.Figure()
        fig = px.line(lineGraph, x="month", y="transactionId", labels = {'month': 'Month', 'transactionId': 'Transactions'}, title = 'Monthwise Transactions via Store')
        fig.update_layout(
            height = 300,)
        st.plotly_chart(fig, use_container_width = True)

    with col2:
        # st.write('Transactions Count on Online')
        # To Calculate Transaction count of Online Visitors
        onlineTransactionCount  = transactionsDf[transactionsDf['modeOfVisit'] == 'Online']['transactionId'].count()
        # st.header(onlineTransactionCount)

        st.markdown("<h5 style='text-align: center;'>Transactions Count on Online</h5>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; '>"+str(onlineTransactionCount)+"</h2>", unsafe_allow_html=True)
        

        lineGraph = pd.DataFrame(transactionsDf[transactionsDf['modeOfVisit']=='Online'].groupby('month').count()['transactionId']).reset_index()
        lineGraph = Sort_Dataframeby_Month(df=lineGraph,monthcolumnname='month')
        fig = go.Figure()
        fig = px.line(lineGraph, x="month", y="transactionId", labels = {'month': 'Month', 'transactionId': 'Transactions'}, title = 'Monthwise Transactions via Online')
        fig.update_layout(
            height = 300,)
        st.plotly_chart(fig, use_container_width = True)
    # st.write('Overall Average units per Customer: Store')
    OverallAvgQuantitySold = pd.DataFrame(transactionsDf.groupby('month').mean()['quantity']).reset_index()
    # st.header(round(OverallAvgQuantitySold['quantity'].mean(),2))

    st.markdown("<h5 style='text-align: center;'>Overall Average units per Customer</h5>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; '>"+str(round(OverallAvgQuantitySold['quantity'].mean(),2))+"</h2>", unsafe_allow_html=True)
        


    OverallAvgQuantitySold = Sort_Dataframeby_Month(pd.DataFrame(transactionsDf.groupby('month').mean()['quantity']).reset_index(), monthcolumnname = 'month')
    fig = go.Figure()
    fig = px.line(OverallAvgQuantitySold, x="month", y="quantity", labels = {'month': 'Month', 'transactionId': 'Transactions'}, title = 'Monthwise Average Units per Customer')
    fig.update_layout(
            height = 300,)
    st.plotly_chart(fig, use_container_width = True)

    col1, col2 = st.columns(2)
    with col1:
        # Average Quantity mean by Store
        # st.write('Average units per Customer: Store')
        # st.header(round(transactionsDf[transactionsDf['modeOfVisit'] == 'Store']['quantity'].mean(), 2))

        st.markdown("<h5 style='text-align: center;'>Average units per Customer: Store</h5>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; '>"+str(round(transactionsDf[transactionsDf['modeOfVisit'] == 'Store']['quantity'].mean(), 2))+"</h2>", unsafe_allow_html=True)
        


        avgQuantityOfStore = Sort_Dataframeby_Month(pd.DataFrame(transactionsDf[transactionsDf['modeOfVisit'] == 'Store'].groupby(['month']).mean()['quantity']).reset_index(), monthcolumnname = 'month')
        fig = go.Figure()
        fig = px.line(avgQuantityOfStore, x="month", y="quantity", labels = {'month': 'Month', 'quantity': 'Average Quantity'}, title = 'Monthwise Average Units per Customer: Store')
        fig.update_layout(
            height = 300,)
        st.plotly_chart(fig, use_container_width = True)

    with col2:  
        # Monthwise Average Quantity by Online DataFrame

        st.markdown("<h5 style='text-align: center;'>Average units per Customer: Online</h5>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; '>"+str(round(transactionsDf[transactionsDf['modeOfVisit'] == 'Online']['quantity'].mean(), 2))+"</h2>", unsafe_allow_html=True)
        
        avgQuantityOfOnline = Sort_Dataframeby_Month(pd.DataFrame(transactionsDf[transactionsDf['modeOfVisit'] == 'Online'].groupby(['month']).mean()['quantity']).reset_index(), monthcolumnname = 'month')
        fig = go.Figure()
        fig = px.line(avgQuantityOfOnline, x="month", y="quantity", labels = {'month': 'Month', 'quantity': 'Average Quantity'}, title = 'Monthwise Average Units per Customer: Online')
        fig.update_layout(
            height = 300,)
        st.plotly_chart(fig, use_container_width = True)



elif sideBarSelection == 'Inventory Control':
    st.markdown("<h2 style='text-align: center; color: black;'>Inventory Control Management</h2>", unsafe_allow_html=True)
    st.markdown("")
    st.markdown("")
    option = st.selectbox('Enter your SKU ID',InventoryDf["SKU ID"].to_list())

    st.markdown("")
    st.markdown("")

    col11, col22, col33,col44 = st.columns(4)
    with col11:
        pr=InventoryDf[InventoryDf["SKU ID"] == option]['Current Stock Quantity']
        for i in pr:
            st.write("Current Stock")
            st.subheader(round(i))

    with col44:
        rp=InventoryDf[InventoryDf["SKU ID"] == option]['Stock Status']
        for i in rp:
            st.write("Status")
            if(i=="Out of Stock"):
                st.markdown("<h3 style='text-align: left; color: red;'>"+i+"</h3>", unsafe_allow_html=True)
            elif(i=="Below Reorder point"):
                st.markdown("<h3 style='text-align: left; color: orange;'>"+i+"</h3>", unsafe_allow_html=True)
            else:
                st.markdown("<h3 style='text-align: left; color: green;'>"+i+"</h3>", unsafe_allow_html=True)

    with col33:
        pr=InventoryDf[InventoryDf["SKU ID"] == option]['Value in WH']
        for i in pr:
            st.write("Item Value")
            st.subheader(f"$ {i:,}")  

    with col22:
        pr=InventoryDf[InventoryDf["SKU ID"] == option]['Revenue Share %']
        for i in pr:
            st.write("Revenue Share %")
            st.subheader(round(i,2))

    col1, col2, col3 = st.columns(3)
    st.markdown("")
    st.markdown("")
    st.markdown("-----------------------------------------------------")

    for i in range(0,len(InventoryDf['Annual Revenue'])):
        InventoryDf['trc']=round((InventoryDf['Annual Revenue'])/ (InventoryDf['Value in WH']),2)

    TR= round((InventoryDf['Annual Revenue'].sum())/ (InventoryDf['Value in WH'].sum()),2)

    sku= InventoryDf['Current Stock Quantity'].sum()

    current_value= round(InventoryDf['Value in WH'].sum(),2)
    count=0
    for i in InventoryDf['Do we need to order?']:
        if(i=='Yes'):
            count=count+1

    col1, col2, col3,col4 = st.columns(4)

    with col1:
        st.write("Total Items")
        st.subheader(f"{round(sku):,}")

    with col2:
        st.write("Turn Over Ratio")
        st.subheader(f" {TR:,}")
    with col3:
        st.write("Value of Items")
        st.subheader(f"$ {current_value:,}")  
    with col4:
        st.write("Reorder Items")
        st.subheader(f"{count:,}")  
    st.markdown("-----------------------------------------------------")
    InventoryDf2=InventoryDf.drop(['SKU ID','Current Stock Quantity','Units (Nos/Kg)','Maximum Lead Time (days)','Unit Price','today',
    'Annual Sale Quantity','Revenue Share %','Cummulative share','Average Weekly Demand','CV','CV rank','Value in WH','ABC rank',
    'Peak Weekly Demand','Safety Stock','Re order point','Do we need to order?','Stock Status','Average Lead Time (days)','SD of Weekly Demand','trc'],axis=1)

    InventoryDf4=InventoryDf.drop(['SKU ID','Annual Revenue','Units (Nos/Kg)','Maximum Lead Time (days)','Unit Price','today',
    'Annual Sale Quantity','Revenue Share %','Cummulative share','Average Weekly Demand','CV','CV rank','Value in WH','ABC rank',
    'Peak Weekly Demand','Safety Stock','Re order point','Do we need to order?','Stock Status','Average Lead Time (days)','SD of Weekly Demand','trc'],axis=1)

    InventoryDf5=InventoryDf.drop(['SKU ID','Annual Revenue','Units (Nos/Kg)','Maximum Lead Time (days)','Unit Price','today',
    'Annual Sale Quantity','Revenue Share %','Cummulative share','Average Weekly Demand','CV','CV rank','Value in WH','ABC rank',
    'Peak Weekly Demand','Safety Stock','Re order point','Do we need to order?','Stock Status','Average Lead Time (days)','SD of Weekly Demand','Current Stock Quantity'],axis=1)
    # InventoryDf3['ASX code'] = InventoryDf2[['ASX code']].copy()
    InventoryDf2=InventoryDf2.groupby(['ABC ?','XYZ ?'],as_index=False)['Annual Revenue'].sum()
    #InventoryDf2.groupby(['ABC ?','XYZ ?']).size().reset_index().groupby('XYZ ?')[[0]].sum()
    InventoryDf4=InventoryDf4.groupby(['ABC ?','XYZ ?'],as_index=False)['Current Stock Quantity'].sum()
    InventoryDf5=InventoryDf5.groupby(['ABC ?','XYZ ?'],as_index=False)['trc'].sum()

    option1 = st.selectbox('',list(set(InventoryDf2["ABC ?"].to_list())))
    st.markdown("")
    st.markdown("")
    pr=InventoryDf2[InventoryDf2["ABC ?"] == option1]
    pr=pr.drop(['ABC ?'],axis=1)
    pr.index.names = [None]

    pr1=InventoryDf4[InventoryDf4["ABC ?"] == option1]
    pr1=pr1.drop(['ABC ?'],axis=1)
    pr1.index.names = [None]

    pr2=InventoryDf5[InventoryDf5["ABC ?"] == option1]
    pr2=pr2.drop(['ABC ?'],axis=1)
    pr2.index.names = [None]

    seg1, seg2, seg3 = st.columns(3)

    with seg1:
        st.markdown("<h5 style='text-align: center; color: black;'>Distribution of Annual Revenue</h5>", unsafe_allow_html=True)
        InventoryDf3 = px.data.tips()
        fig1 = px.bar(InventoryDf3, x=pr["Annual Revenue"].to_list(), y=pr["XYZ ?"].to_list(), orientation='h')
        fig1.update_layout(
            width = 500,
            xaxis_title="Revenue",
            yaxis_title="Demand Status")
        st.plotly_chart(fig1)
    with seg2:
        st.markdown("<h5 style='text-align: center; color: black;'>Distribution of Current Stock</h5>", unsafe_allow_html=True)
        InventoryDf3 = px.data.tips()
        fig1 = px.bar(InventoryDf3, x=pr1["Current Stock Quantity"].to_list(), y=pr1["XYZ ?"].to_list(), orientation='h')
        fig1.update_layout(
            width = 500,
        xaxis_title="Current Quantity",
        yaxis_title="Demand Status")
        st.plotly_chart(fig1)

    with seg3:
        st.markdown("<h5 style='text-align: center; color: black;'>Distribution of Turn Over Ratio</h5>", unsafe_allow_html=True)
        InventoryDf3 = px.data.tips()
        fig1 = px.bar(InventoryDf3, x=pr2["trc"].to_list(), y=pr2["XYZ ?"].to_list(), orientation='h')
        fig1.update_layout(
            width = 500,
        xaxis_title="Turn over Ratio",
        yaxis_title="Demand Status")
        st.plotly_chart(fig1)



    st.markdown("-----------------------------------------------------")

    st.markdown("")
    st.markdown("")


    st.markdown("<h5 style='text-align: center; color: black;'>Distribution Of ABC</h5>", unsafe_allow_html=True)



    InventoryDf1 = px.data.medals_long()

    fig = px.area(InventoryDf, x=InventoryDf['ABC rank'].to_list(), y=InventoryDf["Cummulative share"].to_list(), color=InventoryDf["ABC ?"].to_list() )

    fig.update_layout(
        xaxis_title="Quantity Of Items In Inventory",
        yaxis_title="Revenue Share",
        autosize=True,
        margin=dict(
            l=20,
            r=20,
            b=20,
            t=20,
            pad=6))

    st.plotly_chart(fig, use_container_width = True)


# col1, col2, col3 = st.columns(3)

    st.markdown("-----------------------------------------------------")
elif sideBarSelection == 'Financial Simulator':

    df_revenue['Due Date'] = pd.to_datetime(df_revenue['Due Date'])
    df_expense['Date']=pd.to_datetime(df_expense['Date'])


    df_revenue['Month_Num'] = df_revenue['Due Date'].dt.month

    my_dict={'Month Name':[]}

    for i in range(0,len(df_revenue)):
        my_dict['Month Name'].append(calendar.month_abbr[df_revenue['Month_Num'][i]])

    df_mon=pd.DataFrame.from_dict(my_dict)

    df_revenue['Month Name']=df_mon['Month Name']
    df_revenue.sort_values(by=['Month_Num'])
    df_costprice = pd.merge(df_product, df_revenue, on='Product ID', how='inner')
    df_costprice['Cost Price']= df_costprice['Qty Items'] * df_costprice['Unit Cost']

    my_dict1={'Month Name':[]}
    df_expense['Month_Num'] = df_expense['Date'].dt.month
    for i in range(0,len(df_expense)):
        my_dict1['Month Name'].append(calendar.month_abbr[df_expense['Month_Num'][i]])
    df_mon1=pd.DataFrame.from_dict(my_dict1)
    df_expense['Month Name']=df_mon1['Month Name']
    df_expense_final=df_expense.drop(['Account ID','Date'],axis=1)
    df_expense_final=df_expense.drop(['Account ID','Date'],axis=1)
    df_expense_final=df_expense_final.groupby(['Month Name','Month_Num'],as_index=False).sum()
    df_monwise=df_costprice.drop(['Product ID','Salesperson ID','Product','Group','Category','Supplier','Unit Cost','Order Date','Due Date',
                    'Order Number','Salesperson','Supervisor','Team','Qty Items','Unit Price','Revenue Ac ID','Cost Ac ID','Month_Num'], axis = 1)

    df_monwise=df_monwise.groupby(['Month Name'],as_index=False).sum()


    df_SA = pd.merge(df_monwise, df_expense_final, on='Month Name', how='inner')


    df_SA.columns=['Month','Revenue','Cost Price','Month_Num','Expense']
    df_SA['Operating Income']=df_SA['Revenue']-df_SA['Cost Price']-df_SA['Expense']
    df_SA=df_SA.sort_values(by=['Month_Num'])
    df_SA=df_SA.round(decimals =2)

    rev=df_SA['Revenue'].sum()
    cp=df_SA['Cost Price'].sum()
    ep=df_SA['Expense'].sum()
    inc=df_SA['Operating Income'].sum()
    incp=(100/(df_SA['Revenue']).sum()) * (df_SA['Operating Income'].sum())
    st.markdown("<h2 style='text-align: center; color: black;'>Financial Simulator</h2>", unsafe_allow_html=True)
    st.markdown('')
    st.markdown('')
    st.markdown('')
    col1, col2, col3 = st.columns(3)
    with col1:
        value1 = st.slider(
            'The company Provides the Hike',
            -100, 100,0,5) 
    with col2:
        st.markdown("<h2 style='text-align: center; color: black;'>What IF</h2>", unsafe_allow_html=True)   
    with col3:
            value2 = st.slider(
            'The company change the expense',
            -100, 100,0,5) 
    st.markdown('-------------------------------------------------')
    st.markdown("<h2 style='text-align: center; color: black;'>Metrics</h2>", unsafe_allow_html=True)   
    st.markdown('')

    sec1, sec2, sec3,sec4,sec5 = st.columns(5)
    var_rev=0
    var_cp= round(((1+value1/100) * df_SA['Cost Price'].sum()) - df_SA['Cost Price'].sum(),2)      
    var_exp=  round(((1+value2/100) * df_SA['Expense'].sum()) - df_SA['Expense'].sum(),2)
    var_inc=var_rev-var_cp-var_exp
    var_incp= round((100/df_SA['Operating Income'].sum())* var_inc,2)

    with sec1:
        st.write("Revenue Varience")
        st.subheader(f"$ {var_rev:,}")    

    with sec2:
        st.write("Cost Varience")
        st.subheader(f"$ {var_cp:,}")
    with sec3:
        st.write("Expense Varience")
        st.subheader(f"$ {var_exp:,}")
    with sec4:
        st.write("Income Varience")
        st.subheader(f"$ {var_inc:,}")  
    with sec5:
        st.write("Income % Varience")
        st.subheader(f"{var_incp:} %") 
    st.markdown('-------------------------------------------------')
    st.markdown("<h2 style='text-align: center; color: black;'>Original Metrics</h2>", unsafe_allow_html=True)   
    st.markdown('')

    seg1, seg2, seg3,seg4,seg5 = st.columns(5)

    act_rev= round(df_SA['Revenue'].sum(),2)
    act_cp= df_SA['Cost Price'].sum()    
    act_exp=df_SA['Expense'].sum()
    act_inc=round((act_rev-act_cp-act_exp),2)
    act_incp=round((100/(df_SA['Revenue']).sum()) * (df_SA['Operating Income'].sum()),2)

    with seg1:
        st.write("Actual Revenue")
        st.subheader(f"$ {act_rev:,}")    
    with seg2:
        st.write("Actual Cost")
        st.subheader(f"$ {act_cp:,}")
    with seg3:
        st.write("Actual Expense")
        st.subheader(f"$ {act_exp:,}")
    with seg4:
        st.write("Actual Income")
        st.subheader(f"$ {act_inc:,}")  
    with seg5:
        st.write("Actual Income")
        st.subheader(f"{act_incp:} %") 

    st.markdown('-------------------------------------------------')
    st.markdown("<h2 style='text-align: center; color: black;'>Resultant Metrics</h2>", unsafe_allow_html=True)   
    st.markdown('')
    segm1, segm2, segm3,segm4,segm5 = st.columns(5)
    re_rev= var_rev+act_rev
    re_cp= var_cp+act_cp   
    re_exp=var_exp+act_exp
    re_inc=round((var_inc+act_inc),2)
    re_incp=round((100/re_rev)* re_inc,2)

    with segm1:
        st.write("Resultant Revenue")
        st.subheader(f"$ {re_rev:,}")    
    with segm2:
        st.write("Resultant Cost")
        st.subheader(f"$ {re_cp:,}")
    with segm3:
        st.write("Resultant Expense")
        st.subheader(f"$ {re_exp:,}")
    with segm4:
        st.write("Resultant Income")
        st.subheader(f"$ {re_inc:,}")  
    with segm5:
        st.write("Resultant Income")
        st.subheader(f"{re_incp:} %") 

    st.markdown('-------------------------------------------------')

elif sideBarSelection =='Customer Segmentation':
    st.markdown("<h2 style='text-align: center; color: black;'>Customers Segmentation</h2>", unsafe_allow_html=True)

    option = st.selectbox(
        'Enter The Customer ID',
        df_inv['Cutom er ID'].to_list())
    st.markdown("-----------------------------------------------------------------------")
    st.markdown("")
    st.markdown("")

    sec1,sec2 = st.columns(2)
    with sec1:
        pr=df_inv[df_inv["Cutom er ID"] == option]['first_name']
        for i in pr:
            st.write("Customer Name")
            st.subheader(i)
    with sec2:
        pr=df_inv[df_inv["Cutom er ID"] == option]['email']
        for i in pr:
            st.write("Customer Email")
            st.subheader(i)
    st.markdown("")       
    sec3, sec4 = st.columns(2)       
    with sec3:
        pr=df_inv[df_inv["Cutom er ID"] == option]['Recency Category']
        for i in pr:
            st.write("Recent Purchase")
            st.subheader(i)
    with sec4:
        pr=df_inv[df_inv["Cutom er ID"] == option]['DOB']
        for i in pr:
            st.write("Customer DOB")
            st.subheader(i)

    st.markdown("")
    st.markdown("")
    st.markdown("-----------------------------------------------------------------------")

    sec11, sec22 = st.columns(2)
    with sec11:
        pr=df_inv[df_inv["Cutom er ID"] == option]['Dt_Customer']
        for i in pr:
            st.write("Last Purchase date")
            st.subheader(i)

    with sec22:
        pr=df_inv[df_inv["Cutom er ID"] == option]['Product Name']
        for i in pr:
            st.write("Product Purchased")
            st.subheader(i)
            
    st.markdown("")
    sec33,sec44 = st.columns(2)        
    with sec33:
        pr=df_inv[df_inv["Cutom er ID"] == option]['Sales']
        for i in pr:
            st.write("Purchase Amount")
            st.subheader(i)

    with sec44:
        pr=df_inv[df_inv["Cutom er ID"] == option]['score']
        for i in pr:
            st.write("Purchase Score")
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
        st.markdown("<h5 style='text-align: center; color: black;'>Customers By Education</h5>", unsafe_allow_html=True)

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
            yaxis_title="Education",width = 500),
            
        # st.plotly_chart(fig1)

    with col22:
        st.markdown("<h5 style='text-align: center; color: black;'>Customers By Kid_Flag</h5>", unsafe_allow_html=True)

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
            yaxis_title="Marital Status", width = 500)
        st.plotly_chart(fig1)   

    with col33:
        st.markdown("<h5 style='text-align: center; color: black;'>Customers By Teen_Flag</h5>", unsafe_allow_html=True)

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
        fig.update_layout(width = 400)
        st.plotly_chart(fig)  
    st.markdown("----------------------------------------------")

    col111, col222, col333= st.columns(3)
    with col111:
        st.markdown("<h5 style='text-align: center; color: black;'>Customers By Purchase Recency and Age</h5>", unsafe_allow_html=True)

        df_new1=df_new.drop(['Year_Birth','Education','Marital_Status','Income','Kidhome','Teenhome','Dt_Customer','Age','Income_cat','Recency'],axis=1)
        df_new1=df_new1.groupby(['Recency_cat','Age_cat'],as_index=False)['ID'].count()
        df3 = px.data.iris()

        fig = px.bar(df3, y=df_new1['Recency_cat'].to_list(), x=df_new1["ID"].to_list(),
        color=df_new1['Age_cat'], barmode = 'group',orientation='h')
        fig.update_layout(
            xaxis_title="Count of Customers",
            yaxis_title="Recency",
            width = 500)
        st.plotly_chart(fig)  

    with col222:
        st.markdown("<h5 style='text-align: center; color: black;'>Customers By Income and Age</h5>", unsafe_allow_html=True)

        df_new1=df_new.drop(['Year_Birth','Education','Marital_Status','Income','Kidhome','Teenhome','Dt_Customer','Age','Recency_cat','Recency'],axis=1)
        df_new1=df_new1.groupby(['Income_cat','Age_cat'],as_index=False)['ID'].count()
        df3 = px.data.iris()

        fig = px.bar(df3, x=df_new1['Income_cat'].to_list(), y=df_new1["ID"].to_list(),
        color=df_new1['Age_cat'], barmode = 'group')
        fig.update_layout(
            xaxis_title="Count of Customers",
        yaxis_title="Income Category", width = 500)
        st.plotly_chart(fig)  
    with col333:
        st.markdown("<h5 style='text-align: center; color: black;'>Customers By Age and Age Category</h5>", unsafe_allow_html=True)

        df_new1=df_new.drop(['Year_Birth','Education','Marital_Status','Income','Kidhome','Teenhome','Dt_Customer','Income_cat','Recency_cat','Recency'],axis=1)
        df_new1=df_new1.groupby(['Age','Age_cat'],as_index=False)['ID'].count()
        df3 = px.data.iris()

        fig = px.bar(df3, x=df_new1['Age'].to_list(), y=df_new1["ID"].to_list(),
        color=df_new1['Age_cat'], barmode = 'group')
        fig.update_layout(
            xaxis_title="Age",
            yaxis_title="Count of Customers", width = 450)
        st.plotly_chart(fig)  

    st.markdown("----------------------------------------------")


#-------------------------
else:
    st.write('please select any page')
