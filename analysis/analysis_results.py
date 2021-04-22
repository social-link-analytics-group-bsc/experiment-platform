
# from matplotlib.backends.backend_agg import RendererAgg
import streamlit as st
# import numpy as np
# import pandas as pd
# import xmltodict
# from pandas import json_normalize
# import urllib.request
# import seaborn as sns
# import matplotlib
# from matplotlib.figure import Figure
# from PIL import Image
# import gender_guesser.detector as gender
# from streamlit_lottie import st_lottie
# import requests



# import io
import pandas as pd
import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# import plotly.express as px
# import seaborn as sns
import numpy as np
# import unicodedata
import json

# from collections import defaultdict
# from datetime import timedelta

from prepare_dataset import prep

st.set_page_config(layout="wide")

with open('notis.json') as f:
    notis = json.load(f)
notis_df = pd.DataFrame(notis)

topics = ['salud', 'política', 'mascarillas', 'virus']


df_raw = pd.read_csv('sondea_analisis_20210323_ORIGINAL.csv', sep=";")
df, df_init, df_all, n, fin, ini, read_only_1, read_both, got_to_ans, vars_all, vars_demo, vars_routine = prep(df_raw)


def set_filters(dfall, news):
    st.sidebar.title('Filtro respuestas')

    filt = pd.Series([True]*dfall.shape[0])

    st.sidebar.header('Noticias')
    news_fake_filt_crit = st.sidebar.multiselect('Escoge las fake que quieras filtrar', news[news['is_fake'] == True]['min_title'].values, [], help='Para omitir el filtro no seleccionar ninguna opción')
    news_fake_filt_crit = news[news['min_title'].isin(news_fake_filt_crit)]['news_id'].values
    if len(news_fake_filt_crit) > 0:
        news_fake_filt = dfall['fake_news_id'].isin(news_fake_filt_crit)
        filt &= news_fake_filt

    news_true_filt_crit = st.sidebar.multiselect('Escoge las verdaderas que quieras filtrar', news['min_title'].values, [], help='Para omitir el filtro no seleccionar ninguna opción')
    news_true_filt_crit = news[news['min_title'].isin(news_true_filt_crit)]['news_id'].values
    if len(news_true_filt_crit) > 0:
        news_true_filt = dfall['true_news_id'].isin(news_true_filt_crit)
        filt &= news_true_filt

    news_topic_1_filt_crit = st.sidebar.multiselect('Escoge los tópicos 1 que quieras filtrar', list(set(news['topic_1'].values)), [], help='Para omitir el filtro no seleccionar ninguna opción')
    if len(news_topic_1_filt_crit) > 0:
        topic_1_filt = dfall['fake_topic_1'].isin(news_topic_1_filt_crit) | dfall['true_topic_1'].isin(news_topic_1_filt_crit)
        filt &= topic_1_filt

    news_topic_2_filt_crit = st.sidebar.multiselect('Escoge los tópicos 2 que quieras filtrar', set(news['topic_2'].values), [], help='Para omitir el filtro no seleccionar ninguna opción')
    if len(news_topic_2_filt_crit) > 0:
        topic_2_filt = dfall['fake_topic_2'].isin(news_topic_2_filt_crit) | dfall['true_topic_2'].isin(news_topic_2_filt_crit)
        filt &= topic_2_filt

    st.sidebar.header('Percepción')
    grupos_percepcion = ['Acierto en la verdadera', 'Acierto en la falsa', 'Error en la verdadera', 'Error en la falsa']
    grupos_percep_filt_crit = st.sidebar.multiselect('Escoge el grupo por el que quieras filtrar', grupos_percepcion, [], help='Para omitir el filtro no seleccionar ninguna opción')
    if len(grupos_percep_filt_crit) > 0:
        if 'Acierto en la verdadera' in grupos_percep_filt_crit:
            perce_true_correct_filt = dfall['tysno_verdadera'] == 'sí'
            filt &= perce_true_correct_filt
        if 'Acierto en la falsa' in grupos_percep_filt_crit:
            perce_fake_correct_filt = dfall['fysno_verdadera'] == 'no'
            filt &= perce_fake_correct_filt
        if 'Error en la verdadera' in grupos_percep_filt_crit:
            perce_true_error_filt = dfall['tysno_verdadera'] == 'no'
            filt &= perce_true_error_filt
        if 'Error en la falsa' in grupos_percep_filt_crit:
            perce_fake_error_filt = dfall['fysno_verdadera'] == 'sí'
            filt &= perce_fake_error_filt


    #news_topic_filt
    #grupos_percep_filt

    st.sidebar.title('Filtro demografia')

    st.sidebar.header('Edad')
    edades = ['< 18 años', '18-24 años', '15-34 años', '15-44 años', '15-54 años', '15-65 años', '> 65 años']
    demo_age_filt_crit = st.sidebar.multiselect('Escoge las edades por las que quieras filtrar', edades, [], help='Para omitir el filtro no seleccionar ninguna opción')
    if len(demo_age_filt_crit) > 0:
        demo_age_filt = dfall['dm_edad'].isin(demo_age_filt_crit)
        filt &= demo_age_filt

    st.sidebar.header('Género')
    genero = ['Femenino', 'Masculino', 'No binario', 'NS/NC']
    demo_gen_filt_crit = st.sidebar.multiselect('Escoge el género por el que quieras filtrar', genero, [], help='Para omitir el filtro no seleccionar ninguna opción')
    if len(demo_gen_filt_crit) > 0:
        demo_gen_filt = dfall['dm_genero'].isin(demo_gen_filt_crit)
        filt &= demo_gen_filt

    st.sidebar.header('Estudios')
    st.sidebar.header('Profesional')
    st.sidebar.header('Política')
    st.sidebar.header('Religión')
    st.sidebar.header('Geografia')

    # dm_provincia
    # dm_prov_otro
    #
    # dm_educacion
    # dm_edu_otro
    #
    # dm_professional
    # dm_prof_otro
    #
    # dm_empleo
    # dm_empleo_otro
    #
    # dm_religion
    # dm_rel_otro
    #
    # dm_politica


    return filt


filt = set_filters(df_all, notis_df)
df_all = df_all[filt]

st.title('RRSSalud / Resultados experimento')

sections = ['Ninguna', 'Explorar dataset', 'Comportamiento en plataforma', 'Análisis descriptivo', 'Análisis de percepción', 'Correlaciones']
section = st.selectbox('Qué sección quiere ver?', sections)

if section == 'Explorar dataset':
    st.header(section)
    st.dataframe(df_all)

    st.text('Numero de registros: ' + str(df_all.shape[0]))

    st.text('Description categorical variables')
    st.dataframe(df_all.describe(exclude=[np.number], datetime_is_numeric=True))

    if st.button('Mostrar variables'):
        vars = list(df_all.columns)
        st.text(f"Hay {len(vars)} variables:")
        for idx, var in enumerate(vars):
            st.text(f"{idx + 1}. {var}")


elif section == 'Comportamiento en plataforma':
    st.header(section)

    # st.title('Uso de la plataforma')
    # y = ['Han entrado', 'Han iniciado (y leído la primera noticia)', 'Han leído la segunda noticia', 'Han llegado al formulario', 'Han finalizado']
    # x = [df_all.shape[0], df_all[ini].shape[0], df_all[read_both].shape[0], df_all[got_to_ans].shape[0],
    #      df_all[fin].shape[0]]
    # plt.barh(y, x)
    # for index, value in enumerate(y):
    #     plt.text(x[index], index, str(x[index]))
    # plt.title('Frecuencia de usuarios por estado')
    # st.pyplot(plt.gca().invert_yaxis())

    st.header('Tiempo del experimento')
    # df[df['time_completion_min']<=20]['time_completion_min'].plot.hist()
    fig_time_exp, ax = plt.subplots()
    ax.hist(df_all[df_all['time_completion_min'] <= 20]['time_completion_min'])
    plt.figtext(0.65, 0.6, df_all[df_all['time_completion_min'] <= 20]['time_completion_min'].describe().to_string())
    st.text("Estadisticas descriptivas de tiempo de completitud del experimento (minutos)\n")
    st.pyplot(fig_time_exp)

    st.text("Estadisticas descriptivas de tiempo de lectura de las noticias (segundos)\n")
    fig_time_news, axs = plt.subplots(1, 2, figsize=(15, 5))
    axs[0].hist(df_all[df_all['time_news1'] <= 700]['time_news1'])
    axs[0].title.set_text('News 1')
    plt.figtext(0.35, 0.55, df_all[df_all['time_news1'] <= 700]['time_news1'].describe().to_string())
    axs[1].hist(df_all[df_all['time_news2'] <= 700]['time_news2'])
    axs[1].title.set_text('News 2')
    plt.figtext(0.77, 0.55, df_all[df_all['time_news2'] <= 700]['time_news2'].describe().to_string())
    st.pyplot(fig_time_news)


    st.text("Estadisticas descriptivas de tiempo de lectura de las noticias (segundos)\n")
    fig_time_news_veracity, axs = plt.subplots(1, 2, figsize=(15, 5))

    ft = df_all[df_all['first_true']][['time_news1', 'time_news2']]
    ft.columns = ['true', 'fake']
    ff = df_all[~df_all['first_true']][['time_news1', 'time_news2']]
    ff.columns = ['fake', 'true']
    time_true = pd.concat([ft[['true']], ff[['true']]])
    time_fake = pd.concat([ft[['fake']], ff[['fake']]])

    axs[0].hist(time_true[time_true['true'] <= 700]['true'])
    axs[0].title.set_text('True News')
    plt.figtext(0.35, 0.55, time_true[time_true['true'] <= 700]['true'].describe().to_string())

    axs[1].hist(time_fake[time_fake['fake'] <= 700]['fake'])
    axs[1].title.set_text('Fake News')
    plt.figtext(0.77, 0.55, time_fake[time_fake['fake'] <= 700]['fake'].describe().to_string())
    st.pyplot(fig_time_news_veracity)


    st.text("Estadisticas descriptivas de tiempo de lectura de las noticias (segundos)\n")
    fig_time_news_4, axs = plt.subplots(2, 2, figsize=(15, 10))

    ft = df_all[df_all['first_true']][['time_news1', 'time_news2']]
    ft.columns = ['true', 'fake']
    ff = df_all[~df_all['first_true']][['time_news1', 'time_news2']]
    ff.columns = ['fake', 'true']
    time_true = pd.concat([ft[['true']], ff[['true']]])
    time_fake = pd.concat([ft[['fake']], ff[['fake']]])

    axs[0][0].hist(ft[ft['true'] <= 700]['true'])
    axs[0][0].title.set_text('First News / True')
    plt.figtext(0.35, 0.7, ft[ft['true'] <= 700]['true'].describe().to_string())

    axs[0][1].hist(ff[ff['true'] <= 700]['true'])
    axs[0][1].title.set_text('Second News / True')
    plt.figtext(0.77, 0.7, ff[ff['true'] <= 700]['true'].describe().to_string())

    axs[1][0].hist(ff[ff['fake'] <= 700]['fake'])
    axs[1][0].title.set_text('First News / Fake')
    plt.figtext(0.35, 0.3, ff[ff['fake'] <= 700]['fake'].describe().to_string())

    axs[1][1].hist(ft[ft['fake'] <= 700]['fake'])
    axs[1][1].title.set_text('Second News / Fake')
    plt.figtext(0.77, 0.3, ft[ft['fake'] <= 700]['fake'].describe().to_string())
    st.pyplot(fig_time_news_4)


    st.header('Adjudicación y sensibilidad a noticias')

    true_freq = pd.concat([
        df_all['true_news'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%',
        df_init['true_news'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%',
        df['true_news'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'
    ], axis=1)
    true_freq.columns = ['Adjudicadas', 'Inicializadas', 'Finalizadas']

    fake_freq = pd.concat([
        df_all['fake_news'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%',
        df_init['fake_news'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%',
        df['fake_news'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'
    ], axis=1)
    fake_freq.columns = ['Adjudicadas', 'Inicializadas', 'Finalizadas']

    st.text('Frecuencia adjudicación noticias verdaderas')
    st.dataframe(true_freq[['Inicializadas', 'Finalizadas']])

    st.text('Frecuencia adjudicación noticias falsas')
    st.dataframe(fake_freq[['Adjudicadas', 'Finalizadas']])

    st.text('Probabilidad de finalización del experimento dada una noticia verdadera')
    true_freq_abs = pd.concat([df_init['true_news'].value_counts(), df['true_news'].value_counts()], axis=1)
    true_freq_abs.columns = ['init', 'fin']
    true_freq_abs['prob_fin'] = true_freq_abs['fin'] / true_freq_abs['init']
    true_freq_abs.sort_values('prob_fin', ascending=False)['prob_fin'].mul(100).round(1).astype(str) + '%'

    st.text('Probabilidad de finalización del experimento dada una noticia falsa')
    fake_freq_abs = pd.concat([df_init['fake_news'].value_counts(), df['fake_news'].value_counts()], axis=1)
    fake_freq_abs.columns = ['init', 'fin']
    fake_freq_abs['prob_fin'] = fake_freq_abs['fin'] / fake_freq_abs['init']
    fake_freq_abs.sort_values('prob_fin', ascending=False)['prob_fin'].mul(100).round(1).astype(str) + '%'


elif section == 'Análisis descriptivo':
    st.header(section)

    st.header('Demográfico')

    st.text('Distribución de edad, género, preferencia política y habilidad tecnológica')
    plot_counter = 0
    fig = plt.figure(figsize=(18, 18))
    for var in vars_demo:
        if var in ['dm_genero', 'dm_edad_a', 'dm_politica_a', 'dm_tecnologia']:
            plot_counter += 1
            plt.subplot(2, 2, plot_counter)
            ax = df_all[var].value_counts().plot.bar()
            ax.set_xlabel(var, fontsize=13)
            ax.set_ylabel('Frecuencia', fontsize=13)
            plt.xticks(size=12)
            plt.yticks(size=12)
            plt.grid(False, which='major', axis='x')
            for p in ax.patches:
                h_col = int(p.get_height())
                ax.annotate(f"{h_col} ({round(100 * (h_col / df_all.shape[0]), 1)}%)",
                            (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=12, color='black', xytext=(0, 10),
                            textcoords='offset points')
    st.pyplot(fig)

    st.text('Distribución de residencia')
    fig, ax = plt.subplots()
    var = 'dm_lugar'
    x_label = 'Lugar'
    y_label = 'Frecuencia'
    ax = df_all[var].value_counts().sort_values(ascending=True).plot.barh(figsize=(16, 12))
    ax.set_xlabel(x_label, fontsize=13)
    ax.set_ylabel(y_label, fontsize=13)
    plt.xticks(size=12)
    plt.yticks(size=12)
    plt.grid(False, which='major', axis='x')
    for p in ax.patches:
        w_col = int(p.get_width())
        ax.annotate(f"{w_col} ({round(100 * (w_col / df_all.shape[0]), 1)}%)", (p.get_x() + p.get_width() + 2.8, p.get_y() - 0.5),
                    ha='center', va='center', fontsize=12, color='black', xytext=(0, 10),
                    textcoords='offset points')
    st.pyplot(fig)

    st.text('Distribución de nivel formativo')
    fig, ax = plt.subplots()
    var = 'dm_education'
    x_label = 'Educación'
    y_label = 'Frecuencia'
    ax = df_all[var].value_counts().sort_values(ascending=True).plot.barh()
    ax.set_xlabel(x_label, fontsize=13)
    ax.set_ylabel(y_label, fontsize=13)
    plt.xticks(size=12)
    plt.yticks(size=12)
    plt.grid(False, which='major', axis='x')
    for p in ax.patches:
        w_col = int(p.get_width())
        ax.annotate(f"{w_col} ({round(100 * (w_col / df_all.shape[0]), 1)}%)", (p.get_x() + p.get_width(), p.get_y()),
                    ha='center', va='center', fontsize=12, color='black', xytext=(40, 10),
                    textcoords='offset points')
    st.pyplot(fig)

    st.text('Distribución de situación laboral')
    fig, ax = plt.subplots()
    var = 'dm_empleo'
    x_label = 'Empleo'
    y_label = 'Frecuencia'
    ax = df_all[var].value_counts().sort_values(ascending=True).plot.barh()
    ax.set_xlabel(x_label, fontsize=13)
    ax.set_ylabel(y_label, fontsize=13)
    plt.xticks(size=12)
    plt.yticks(size=12)
    plt.grid(False, which='major', axis='x')
    for p in ax.patches:
        w_col = int(p.get_width())
        ax.annotate(f"{w_col} ({round(100 * (w_col / df_all.shape[0]), 1)}%)", (p.get_x() + p.get_width(), p.get_y()),
                    ha='center', va='center', fontsize=12, color='black', xytext=(40, 10),
                    textcoords='offset points')
    st.pyplot(fig)

    st.text('Distribución de preferencia religiosa')
    fig, ax = plt.subplots()
    var = 'dm_religion'
    x_label = 'Preferencia religiosa'
    y_label = 'Frecuencia'
    ax = df_all[var].value_counts().sort_values(ascending=True).plot.barh()
    ax.set_xlabel(x_label, fontsize=13)
    ax.set_ylabel(y_label, fontsize=13)
    plt.xticks(size=12)
    plt.yticks(size=12)
    plt.grid(False, which='major', axis='x')
    for p in ax.patches:
        w_col = int(p.get_width())
        ax.annotate(f"{w_col} ({round(100 * (w_col / df_all.shape[0]), 1)}%)", (p.get_x() + p.get_width(), p.get_y()),
                    ha='center', va='center', fontsize=12, color='black', xytext=(40, 10),
                    textcoords='offset points')
    st.pyplot(fig)

    st.header('Hábitos informativos')
    # Prepare data
    category_names = ['Diario', 'Algunas veces en la semana', 'Algunas veces al mes', 'Algunas veces en los últimos 12 meses', 'Nunca', 'NS/NC']
    results = dict()
    for var in vars_routine:
        key = var.split('_')[1].title()
        results[key] = list()
        routine = dict(df_all[var].value_counts())
        for category_name in category_names:
            if category_name in routine:
                results[key].append(routine[category_name])
            else:
                results[key].append(0)


    def routine_responses(results, category_names):
        """
        Parameters
        ----------
        results : dict
            A mapping from question labels to a list of answers per category.
            It is assumed all lists contain the same number of entries and that
            it matches the length of *category_names*.
        category_names : list of str
            The category labels.
        """
        labels = list(results.keys())
        data = np.array(list(results.values()))
        data_cum = data.cumsum(axis=1)
        category_colors = plt.get_cmap('RdYlGn')(
            np.linspace(0.15, 0.85, data.shape[1]))

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.invert_yaxis()
        ax.xaxis.set_visible(False)
        ax.set_xlim(0, np.sum(data, axis=1).max())

        for i, (colname, color) in enumerate(zip(category_names, category_colors)):
            widths = data[:, i]
            starts = data_cum[:, i] - widths
            ax.barh(labels, widths, left=starts, height=0.5,
                    label=colname, color=color)
            xcenters = starts + widths / 2

            r, g, b, _ = color
            text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
            for y, (x, c) in enumerate(zip(xcenters, widths)):
                if int(c) == 0:
                    continue
                ax.text(x, y, f"{str(int(c))}", ha='center', va='center',
                        color=text_color)
        ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
                  loc='lower left', fontsize='small')

        return fig, ax


    fig, ax = routine_responses(results, category_names)
    st.pyplot(fig)


elif section == 'Análisis de percepción':
    st.header(section)

    st.header('Percepción vericidad')

    st.markdown('Respuesta sobre noticia **`falsa`** adjudicada')
    fig, ax = plt.subplots()
    ax = df_all['fysno_verdadera'].value_counts().plot.bar()
    ax.set_xlabel('¿Cree que es verdadera la noticia [falsa]?', fontsize=13)
    ax.set_ylabel('Frecuencia', fontsize=13)
    plt.xticks(size=12, rotation=0)
    plt.yticks(size=12)
    plt.grid(False, which='major', axis='x')
    for p in ax.patches:
        h_col = int(p.get_height())
        ax.annotate(f"{h_col} ({round(100 * (h_col / df_all.shape[0]), 1)}%)", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=12, color='black', xytext=(0, 10),
                    textcoords='offset points')
    st.pyplot(fig)


    st.markdown('Noticias **`falsas`** ordenadas por errores en detección ')
    fake_news_names = list(df_all['fake_news'].unique())
    rights, rights_str, wrongs, wrongs_str = [], [], [], []
    for name in fake_news_names:
        errors = df_all.loc[(df_all['fake_news'] == name) & (df_all['fysno_verdadera'] == 'sí'), :].shape[0] / \
                 df_all.loc[df_all['fake_news'] == name, :].shape[0]
        no_errors = df_all.loc[(df_all['fake_news'] == name) & (df_all['fysno_verdadera'] == 'no'), :].shape[0] / \
                    df_all.loc[df_all['fake_news'] == name, :].shape[0]
        wrongs.append(round(errors * 100, 1))
        wrongs_str.append(str(round(errors * 100, 1)) + '%')
        rights.append(round(no_errors * 100, 1))
        rights_str.append(str(round(no_errors * 100, 1)) + '%')
    fake_news_df = pd.DataFrame.from_dict(
        {'Noticia falsa': fake_news_names, 'Marcada como verdadera (Error)': wrongs_str,
         'Marcada como falsa (Acierto)': rights_str, 'wrong': wrongs, 'rights': rights})
    fake_news_df.sort_values(by='wrong', ascending=False, ignore_index=True, inplace=True)
    st.dataframe(fake_news_df[['Noticia falsa', 'Marcada como verdadera (Error)', 'Marcada como falsa (Acierto)']])

    st.markdown('Respuesta sobre noticia **`verdadera`** adjudicada')
    fig, ax = plt.subplots()
    ax = df_all['tysno_verdadera'].value_counts().plot.bar()
    ax.set_xlabel('¿Cree que es verdadera la noticia [verdadera]?', fontsize=13)
    ax.set_ylabel('Frecuencia', fontsize=13)
    plt.xticks(size=12, rotation=0)
    plt.yticks(size=12)
    plt.grid(False, which='major', axis='x')
    for p in ax.patches:
        h_col = int(p.get_height())
        ax.annotate(f"{h_col} ({round(100 * (h_col / df_all.shape[0]), 1)}%)", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=12, color='black', xytext=(0, 10),
                    textcoords='offset points')
    st.pyplot(fig)

    st.markdown('Noticias **`verdaderas`** ordenadas por errores en detección ')
    news_names = list(df_all['true_news'].unique())
    rights, rights_str, wrongs, wrongs_str = [], [], [], []
    for name in news_names:
        errors = df_all.loc[(df_all['true_news'] == name) & (df_all['tysno_verdadera'] == 'no'), :].shape[0] / \
                 df_all.loc[df_all['true_news'] == name, :].shape[0]
        no_errors = df_all.loc[(df_all['true_news'] == name) & (df_all['tysno_verdadera'] == 'sí'), :].shape[0] / \
                    df_all.loc[df_all['true_news'] == name, :].shape[0]
        wrongs.append(round(errors * 100, 1))
        wrongs_str.append(str(round(errors * 100, 1)) + '%')
        rights.append(round(no_errors * 100, 1))
        rights_str.append(str(round(no_errors * 100, 1)) + '%')
    news_df = pd.DataFrame.from_dict({'Noticia verdadera': news_names, 'Marcada como falsa (Error)': wrongs_str,
                                      'Marcada como verdadera (Acierto)': rights_str, 'wrong': wrongs,
                                      'rights': rights})
    news_df.sort_values(by='wrong', ascending=False, ignore_index=True, inplace=True)
    st.dataframe(news_df[['Noticia verdadera', 'Marcada como falsa (Error)', 'Marcada como verdadera (Acierto)']])

    st.header('Análisis de justificaciones')

    st.markdown('Justificaciones sobre noticias **`falsas`** marcadas como *`verdaderas`*')
    vars_justifications_fake_checked_true = [
        'fys_recuerda_leida',
        'fys_medio_conocido',
        'fys_medio_fiable',
        'fys_fuentes_conocidas',
        'fys_fuentes_confiables',
        'fys_abordaje_serio',
        'fys_coherente',
        'fys_concuerda_creencias',
        'fys_alineado_ideologia',
        'fys_otro'
    ]
    justifications = []
    num_justifications = []
    num_justifications_str = []
    for var in vars_justifications_fake_checked_true:
        justifications.append(' '.join(var.split('_')[1:]))
        num_just = round(df_all.loc[(df_all['fysno_verdadera'] == 'sí') & (df_all[var] == 'checked'), :].shape[0] /
                         df_all.loc[df_all['fysno_verdadera'] == 'sí', :].shape[0] * 100, 1)
        num_justifications.append(num_just)
        num_justifications_str.append(str(num_just) + '%')
    justifications_df = pd.DataFrame.from_dict(
        {'Justificacion': justifications, 'Num. Seleccion': num_justifications_str, 'num_just': num_justifications})
    justifications_df.sort_values(by='num_just', ignore_index=True, inplace=True, ascending=False)
    st.dataframe(justifications_df[['Justificacion', 'Num. Seleccion']].head(10))

    st.markdown('Justificaciones sobre noticias **`falsas`** marcadas como *`falsas`*')
    vars_justifications_fake_checked_false = [
        'fno_aclaracion_desmintiendo',
        'fno_medio_desconocido',
        'fno_medio_poco_fiable',
        'fno_fuentes_desconocidas',
        'fno_fuentes_no_confiables',
        'fno_sin_fuentes',
        'fno_abordaje_no_serio',
        'fno_no_coherente',
        'fno_titulo_sensacionalista',
        'fno_imagen_sensacionalista',
        'fno_no_concuerda_creencias',
        'fno_no_alineado_ideologia',
        'fno_otro'
    ]
    justifications = []
    num_justifications = []
    num_justifications_str = []
    for var in vars_justifications_fake_checked_false:
        justifications.append(' '.join(var.split('_')[1:]))
        num_just = round(df_all.loc[(df_all['fysno_verdadera'] == 'no') & (df_all[var] == 'checked'), :].shape[0] /
                         df_all.loc[df_all['fysno_verdadera'] == 'no', :].shape[0] * 100, 1)
        num_justifications.append(num_just)
        num_justifications_str.append(str(num_just) + '%')
    justifications_df = pd.DataFrame.from_dict(
        {'Justificacion': justifications, 'Num. Seleccion': num_justifications_str, 'num_just': num_justifications})
    justifications_df.sort_values(by='num_just', ignore_index=True, inplace=True, ascending=False)
    st.dataframe(justifications_df[['Justificacion', 'Num. Seleccion']].head(10))

    st.markdown('Justificaciones sobre noticias **`verdaderas`** marcadas como *`falsas`*')
    vars_justifications_true_checked_false = [
        'tno_aclaracion_desmintiendo',
        'tno_medio_desconocido',
        'tno_medio_poco_fiable',
        'tno_fuentes_desconocidas',
        'tno_fuentes_no_confiables',
        'tno_sin_fuentes',
        'tno_abordaje_no_serio',
        'tno_no_coherente',
        'tno_titulo_sensacionalista',
        'tno_imagen_sensacionalista',
        'tno_no_concuerda_creencias',
        'tno_no_alineado_ideologia',
        'tno_otro'
    ]
    justifications = []
    num_justifications = []
    num_justifications_str = []
    for var in vars_justifications_true_checked_false:
        justifications.append(' '.join(var.split('_')[1:]))
        num_just = round(df_all.loc[(df_all['tysno_verdadera'] == 'no') & (df_all[var] == 'checked'), :].shape[0] /
                         df_all.loc[df_all['tysno_verdadera'] == 'no', :].shape[0] * 100, 1)
        num_justifications.append(num_just)
        num_justifications_str.append(str(num_just) + '%')
    justifications_df = pd.DataFrame.from_dict(
        {'Justificacion': justifications, 'Num. Seleccion': num_justifications_str, 'num_just': num_justifications})
    justifications_df.sort_values(by='num_just', ignore_index=True, inplace=True, ascending=False)
    st.dataframe(justifications_df[['Justificacion', 'Num. Seleccion']].head(len(justifications)))

    st.markdown('Justificaciones sobre noticias **`verdaderas`** marcadas como *`verdadera`*')
    vars_justifications_true_checked_true = [
        'tys_recuerda_leida',
        'tys_medio_comunicacion_conocido',
        'tys_medio_comunicacion_fiable',
        'tys_fuentes_conocidas',
        'tys_fuentes_confiables',
        'tys_abordaje_serio',
        'tys_coherente',
        'tys_concuerda_creencias',
        'tys_alineado_ideologia',
        'tys_otro'
    ]
    justifications = []
    num_justifications = []
    num_justifications_str = []
    for var in vars_justifications_true_checked_true:
        justifications.append(' '.join(var.split('_')[1:]))
        num_just = round(df_all.loc[(df_all['tysno_verdadera'] == 'sí') & (df_all[var] == 'checked'), :].shape[0] /
                         df_all.loc[df_all['tysno_verdadera'] == 'sí', :].shape[0] * 100, 1)
        num_justifications.append(num_just)
        num_justifications_str.append(str(num_just) + '%')
    justifications_df = pd.DataFrame.from_dict(
        {'Justificacion': justifications, 'Num. Seleccion': num_justifications_str, 'num_just': num_justifications})
    justifications_df.sort_values(by='num_just', ignore_index=True, inplace=True, ascending=False)
    st.dataframe(justifications_df[['Justificacion', 'Num. Seleccion']].head(len(justifications)))

    st.header('Análisis de acciones')

    st.markdown('Acciones en noticias falsas')
    vars_actions_checked_false = [
        'faf_compartira_familia_amigos',
        'faf_publicara_redes',
        'faf_consultara_fuentes',
        'faf_aplicara_aprendido',
        'faf_no_accion'
    ]
    actions = []
    num_actions = []
    num_actions_str = []
    for var in vars_actions_checked_false:
        actions.append(' '.join(var.split('_')[1:]))
        num_act = round(df_all.loc[df_all[var] == 'checked', :].shape[0] / df_all.loc[df_all[var] != '-', :].shape[0] * 100, 1)
        num_actions.append(num_act)
        num_actions_str.append(str(num_act) + '%')
    actions_df = pd.DataFrame.from_dict({'Actions': actions, 'Num. Seleccion': num_actions_str, 'num_act': num_actions})
    actions_df.sort_values(by='num_act', ignore_index=True, inplace=True, ascending=False)
    st.dataframe(actions_df[['Actions', 'Num. Seleccion']].head(len(actions)))

    st.markdown('Acciones en noticias verdaderas')
    vars_actions_checked_true = [
        'taf_compartira_familia_amigos',
        'taf_publicara_redes',
        'taf_consultara_fuentes',
        'taf_aplicara_aprendido',
        'taf_no_accion'
    ]
    actions = []
    num_actions = []
    num_actions_str = []
    for var in vars_actions_checked_true:
        actions.append(' '.join(var.split('_')[1:]))
        num_act = round(df_all.loc[df_all[var] == 'checked', :].shape[0] / df_all.loc[df_all[var] != '-', :].shape[0] * 100, 1)
        num_actions.append(num_act)
        num_actions_str.append(str(num_act) + '%')
    actions_df = pd.DataFrame.from_dict({'Actions': actions, 'Num. Seleccion': num_actions_str, 'num_act': num_actions})
    actions_df.sort_values(by='num_act', ignore_index=True, inplace=True, ascending=False)
    st.dataframe(actions_df[['Actions', 'Num. Seleccion']].head(len(actions)))


elif section == 'Correlaciones':
    st.header(section)









