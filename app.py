import streamlit as st
import pandas as pnd
import plotly.express as px
import matplotlib.pyplot as plt
st.set_page_config(page_title='Экономика РФ: 2000-2025',page_icon='📝',layout='wide')
data=pnd.read_excel('https://raw.githubusercontent.com/crazyabbook/datasets/main/economy.xlsx')


st.title('📝 Анализ динамики экономических показателей Российской Федерации за 2000-2025 гг.')
st.subheader('Сравнительный анализ среднемесячных заработных плат в сферах строительства, образования и гостинично-ресторанного бизнеса: как ВВП, инфляция и безработица формировали финансовую динамику последних лет.')
st.subheader('Показатели номинальных заработных плат по отраслям экономики за весь период.')
st.dataframe(data)
st.subheader('Показатели номинальных заработных плат по отраслям за период 2000 и 2025 гг.')
salary_2000=data[data['Год']==2000].iloc[0]
salary_2025=data[data['Год']==2025].iloc[0]
sectors=['Строительство','Образование','Гостинично-ресторанный бизнес']
columns=[f'НЗП {sector}, ₽' for sector in sectors]
data_2000=pnd.DataFrame({'Отрасль':sectors,'Зарплата':[salary_2000[col] for col in columns],'Год':'2000'})
data_2025=pnd.DataFrame({'Отрасль':sectors,'Зарплата':[salary_2025[col] for col in columns],'Год':'2025'})
chart_2000=px.bar(data_2000,x='Отрасль',y='Зарплата',title='<b>2000 год</b>',color_discrete_sequence=['#FF6B6B'],labels={'Зарплата':'Заработная плата, ₽','Отрасль':'Отрасль экономики'})
chart_2025=px.bar(data_2025,x='Отрасль',y='Зарплата',title='<b>2025 год</b>',color_discrete_sequence=['#4ECDC4'],labels={'Зарплата':'Заработная плата, ₽','Отрасль':'Отрасль экономики'})
chart_2000.update_layout(title_x=0.5,title_font_size=20)
chart_2025.update_layout(title_x=0.5,title_font_size=20)
col1,col2=st.columns(2)
with col1:
  st.plotly_chart(chart_2000,use_container_width=True)
with col2:
  st.plotly_chart(chart_2025,use_container_width=True)
st.markdown('---')


data['РЗП Строительство, ₽']=data['НЗП Строительство, ₽']/(1+data['Инфляция, %']/100)
data['РЗП Образование, ₽']=data['НЗП Образование, ₽']/(1+data['Инфляция, %']/100)
data['РЗП Гостинично-ресторанный бизнес, ₽']=data['НЗП Гостинично-ресторанный бизнес, ₽']/(1+data['Инфляция, %']/100)


st.header('Анализ сферы «Строительство»')
st.subheader('📎 Динамика номинальной и реальной заработной платы.')
chart=px.line(data,x='Год',y=['НЗП Строительство, ₽','РЗП Строительство, ₽'],labels={'Год':'Год','value':'Заработная плата, ₽','variable':'Показатели:'},color_discrete_sequence=['#4ECDC4','#FF4500'],line_shape='spline')
chart.add_scatter(x=data['Год'],y=data['Инфляция, %'],name='Инфляция, %',line=dict(color='#808080',dash='dash'),yaxis='y2')
chart.add_scatter(x=data['Год'],y=data['Безработица, %'],name='Безработица, %',line=dict(color='#D35400',dash='dot'),yaxis='y2')
chart.update_layout(xaxis_title_font=dict(size=18),yaxis_title_font=dict(size=18),legend=dict(font=dict(size=16),title=dict(font=dict(size=18)),x=1.1,),yaxis2=dict(overlaying='y',side='right',showgrid=False))
chart.update_xaxes(showgrid=True)
chart.for_each_trace(lambda t:t.update(name='Номинальная заработная плата, ₽' if 'НЗП' in t.name else 'Реальная заработная плата, ₽' if 'РЗП' in t.name else t.name))
st.plotly_chart(chart)
if st.button('Справка «Строительство» – динамика.'):
  st.info('''Номинальная заработная плата выросла с 2,6 тыс. ₽ до 98,6 тыс. ₽, то есть в ~37 раз.

  Реальная заработная плата росла с замедлением в кризисные годы: 2009, 2015, 2020, 2022 гг.''')
st.subheader('📎 Корреляция реальной заработной платы с экономическими показателями.')
corr_columns=['РЗП Строительство, ₽','ВВП, млрд ₽','Инфляция, %','Безработица, %']
corr_matrix=data[corr_columns].corr()
target_row=corr_matrix.loc['РЗП Строительство, ₽',:]
target_row=target_row.drop('РЗП Строительство, ₽')
corr_1d=pnd.DataFrame([target_row],columns=target_row.index)
fig=px.imshow(corr_1d,text_auto='.2f',color_continuous_scale='Teal',labels=dict(x='',y='',),aspect='auto')
fig.update_traces(textfont=dict(size=18))
fig.update_xaxes(showticklabels=True,tickfont=dict(size=14))
fig.update_yaxes(showticklabels=False)
fig.update_coloraxes(colorbar_title_font_size=14,colorbar_tickfont_size=12)
st.plotly_chart(fig, use_container_width=True)
if st.button('Справка «Строительство» – корреляция.'):
  st.info('''РЗП-ВВП (0,99) – очень сильная прямая зависимость: чем выше ВВП, тем выше РЗП.

  РЗП-Инфляция (-0,51) – умеренная обратная зависимость: чем выше инфляция, тем ниже РЗП.
  
  РЗП-Безработица (-0,91) – очень сильная обратная зависимость: чем выше безработица, тем ниже РЗП.''')
st.markdown('---')


st.header('Анализ сферы «Образование»')
st.subheader('📎 Динамика номинальной и реальной заработной платы.')
chart=px.line(data,x='Год',y=['НЗП Образование, ₽','РЗП Образование, ₽'],labels={'Год':'Год','value':'Заработная плата, ₽','variable':'Показатели:'},color_discrete_sequence=['#4ECDC4','#FF4500'],line_shape='spline')
chart.add_scatter(x=data['Год'],y=data['Инфляция, %'],name='Инфляция, %',line=dict(color='#808080',dash='dash'),yaxis='y2')
chart.add_scatter(x=data['Год'],y=data['Безработица, %'],name='Безработица, %',line=dict(color='#D35400',dash='dot'),yaxis='y2')
chart.update_layout(xaxis_title_font=dict(size=18),yaxis_title_font=dict(size=18),legend=dict(font=dict(size=16),title=dict(font=dict(size=18)),x=1.1,),yaxis2=dict(overlaying='y',side='right',showgrid=False))
chart.update_xaxes(showgrid=True)
chart.for_each_trace(lambda t:t.update(name='Номинальная заработная плата, ₽' if 'НЗП' in t.name else 'Реальная заработная плата, ₽' if 'РЗП' in t.name else t.name))
st.plotly_chart(chart)
if st.button('Справка «Образование» – динамика.'):
  st.info('''Номинальная заработная плата выросла с 1,2 тыс. ₽ до 71,3 тыс. ₽, то есть в ~58 раз.
  
  Реальная заработная плата росла с замедлением в кризисные годы: 2010, 2015, 2020, 2022 гг.''')
st.subheader('📎 Корреляция реальной заработной платы с экономическими показателями.')
corr_columns=['РЗП Образование, ₽','ВВП, млрд ₽','Инфляция, %','Безработица, %']
corr_matrix=data[corr_columns].corr()
target_row=corr_matrix.loc['РЗП Образование, ₽',:]
target_row=target_row.drop('РЗП Образование, ₽')
corr_1d=pnd.DataFrame([target_row],columns=target_row.index)
fig=px.imshow(corr_1d,text_auto='.2f',color_continuous_scale='Teal',labels=dict(x='',y='',),aspect='auto')
fig.update_traces(textfont=dict(size=18))
fig.update_xaxes(showticklabels=True,tickfont=dict(size=14))
fig.update_yaxes(showticklabels=False)
fig.update_coloraxes(colorbar_title_font_size=14,colorbar_tickfont_size=12)
st.plotly_chart(fig, use_container_width=True)
if st.button('Справка «Образование» – корреляция.'):
  st.info('''РЗП-ВВП (0,99) – очень сильная прямая зависимость: чем выше ВВП, тем выше РЗП.

  РЗП-Инфляция (-0,56) – умеренная обратная зависимость: чем выше инфляция, тем ниже РЗП.
  
  РЗП-Безработица (-0,91) – очень сильная обратная зависимость: чем выше безработица, тем ниже РЗП.''')
st.markdown('---')


st.header('Анализ сферы «Гостинично-ресторанный бизнес»')
st.subheader('📎 Динамика номинальной и реальной заработной платы.')
chart=px.line(data,x='Год',y=['НЗП Гостинично-ресторанный бизнес, ₽','РЗП Гостинично-ресторанный бизнес, ₽'],labels={'Год':'Год','value':'Заработная плата, ₽','variable':'Показатели:'},color_discrete_sequence=['#4ECDC4','#FF4500'],line_shape='spline')
chart.add_scatter(x=data['Год'],y=data['Инфляция, %'],name='Инфляция, %',line=dict(color='#808080',dash='dash'),yaxis='y2')
chart.add_scatter(x=data['Год'],y=data['Безработица, %'],name='Безработица, %',line=dict(color='#D35400',dash='dot'),yaxis='y2')
chart.update_layout(xaxis_title_font=dict(size=18),yaxis_title_font=dict(size=18),legend=dict(font=dict(size=16),title=dict(font=dict(size=18)),x=1.1,),yaxis2=dict(overlaying='y',side='right',showgrid=False))
chart.update_xaxes(showgrid=True)
chart.for_each_trace(lambda t:t.update(name='Номинальная заработная плата, ₽' if 'НЗП' in t.name else 'Реальная заработная плата, ₽' if 'РЗП' in t.name else t.name))
st.plotly_chart(chart)
if st.button('Справка «Гостинично-ресторанный бизнес» – динамика.'):
  st.info('''Номинальная заработная плата выросла с 1,6 тыс. ₽ до 61,9 тыс. ₽, то есть в ~38 раз.

  Реальная заработная плата росла с замедлением в кризисные годы: 2015, 2020, 2022 гг.''')
st.subheader('📎 Корреляция реальной заработной платы с экономическими показателями.')
corr_columns=['РЗП Гостинично-ресторанный бизнес, ₽','ВВП, млрд ₽','Инфляция, %','Безработица, %']
corr_matrix=data[corr_columns].corr()
target_row=corr_matrix.loc['РЗП Гостинично-ресторанный бизнес, ₽',:]
target_row=target_row.drop('РЗП Гостинично-ресторанный бизнес, ₽')
corr_1d=pnd.DataFrame([target_row],columns=target_row.index)
fig=px.imshow(corr_1d,text_auto='.2f',color_continuous_scale='Teal',labels=dict(x='',y='',),aspect='auto')
fig.update_traces(textfont=dict(size=18))
fig.update_xaxes(showticklabels=True,tickfont=dict(size=14))
fig.update_yaxes(showticklabels=False)
fig.update_coloraxes(colorbar_title_font_size=14,colorbar_tickfont_size=12)
st.plotly_chart(fig, use_container_width=True)
if st.button('Справка «Гостинично-ресторанный бизнес» – корреляция.'):
  st.info('''РЗП-ВВП (0,99) – очень сильная прямая зависимость: чем выше ВВП, тем выше РЗП.

  РЗП-Инфляция (-0,53) – умеренная обратная зависимость: чем выше инфляция, тем ниже РЗП.
  
  РЗП-Безработица (-0,91) – очень сильная обратная зависимость: чем выше безработица, тем ниже РЗП.''')
st.markdown('---')


st.subheader('Краткие итоги:')
st.markdown('Все три отрасли экономики продемонстрировали относительно устойчивый рост заработной платы с 2000 по 2025 гг. Колебания возникали в ответ на изменение темпов ВВП, инфляции и безработицы.')
st.markdown('🔴 Строительство:')
st.markdown('НЗП: 2,6 тыс. ₽ – 98,6 тыс. ₽ (рост ~37 раз)')
st.markdown('🔴 Образование:')
st.markdown('НЗП: 1,2 тыс. ₽ – 71,3 тыс. ₽ (рост ~58 раз)')
st.markdown('🔴 Гостинично-ресторанный бизнес:')
st.markdown('НЗП: 1,6 тыс. ₽ – 61,9 тыс. ₽ (рост ~38 раз)')
st.markdown('Реальные зарплаты во всех трех отраслях отличаются очень сильной прямой зависимостью от ВВП и очень сильной обратной зависимостью от безработицы. Наиболее защищенной от инфляции оказалась сфера «Строительство», наименее защищенной – сфера «Образование».')
st.markdown('Согласно общей тенденции, с 2022 г. наблюдается согласованное улучшение доходов, обусловленное ростом ВВП и снижением безработицы.')
st.markdown('---')


if st.button('Завершить'):
  st.balloons()
  st.success('🏆 Поздравляем, вы успешно ознакомились с отчетом!')