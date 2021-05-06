# from matplotlib.backends.backend_agg import RendererAgg
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# import unicodedata
import json

from prepare_dataset import prep

st.set_page_config(layout="wide")

with open("notis.json") as f:
    notis = json.load(f)
notis_df = pd.DataFrame(notis)

topics = ["salud", "política", "mascarillas", "virus"]


df_raw = pd.read_csv("./data/sondea_analisis_20210323_SONDEA.csv", sep=";")
(
    df,
    df_init,
    df_all,
    n,
    fin,
    ini,
    read_only_1,
    read_both,
    got_to_ans,
    vars_all,
    vars_demo,
    vars_routine,
) = prep(df_raw)

val_edad = [
    "< 18 años",
    "18-24 años",
    "25-34 años",
    "35-44 años",
    "45-54 años",
    "55-65 años",
    "> 65 años",
]
val_genero = ["Femenino", "Masculino", "No binario", "NS/NC"]
val_estudios = [
    "No tiene estudios en educación formal",
    "Primaria",
    "Secundaria",
    "Formación Profesional",
    "Grado/Licenciatura",
    "Posgrado",
    "Master",
    "Doctorado",
    "Otro",
    "NS/NC",
]
val_tecno = ["Básica", "Media", "Avanzada", "NS/NC"]
val_professional = [
    "No estoy trabajando",
    "Administración Pública y defensa",
    "Actividades artísticas, recreativas y de entretenimiento",
    "Actividades profesionales, científicas y técnicas",
    "Actividades administrativas y servicios auxiliares",
    "Actividades financieras y de seguros",
    "Agricultura y ganadería, silvicultura y pesca",
    "Actividades inmobiliarias",
    "Construcción",
    "Comercio",
    "Empleo doméstico",
    "Educación",
    "Hostelería",
    "Industria",
    "Información y comunicaciones",
    "Minería",
    "Sanidad y servicios sociales",
    "Suministro de energía eléctrica, gas, vapor y aire acondicionado",
    "Suministro de agua y saneamiento",
    "Suministro de telefonía",
    "Transporte",
    "Otro",
]
val_empleo = [
    "Contrato a tiempo completo",
    "Contrato a tiempo parcial",
    "Contrato por horas",
    "Autónomo o por cuenta propia",
    "Desempleado",
    "Estudiante",
    "Jubilado",
    "Labores de hogar",
    "No trabaja",
    "No trabaja",
    "Otro",
    "NS/NC",
]
val_politica = [
    "Izquierda",
    "Centro izquierda",
    "Centro",
    "Centro derecha",
    "Derecha",
    "NS/NC",
]
val_religion = [
    "Católico",
    "Evangélico",
    "Protestante",
    "Judío",
    "Islámico",
    "Budista",
    "Agnóstico",
    "Ateo",
    "Otro",
    "NS/NC",
]
val_provincia = [
    "Fuera de España",
    "Albacete",
    "Alacant",
    "Almería",
    "Araba",
    "Asturias",
    "Ávila",
    "Badajoz",
    "Balears / Illes Balears",
    "Barcelona",
    "Bizkaia",
    "Burgos",
    "Cáceres",
    "Cádiz",
    "Cantabria",
    "Castelló",
    "Ceuta",
    "Ciudad Real",
    "Córdoba",
    "A Coruña",
    "Cuenca",
    "Gipuzkoa",
    "Girona",
    "Granada",
    "Guadalajara",
    "Huelva",
    "Huesca",
    "Jaén",
    "León",
    "Lleida",
    "Lugo",
    "Madrid",
    "Málaga",
    "Melilla",
    "Murcia",
    "Navarra",
    "Ourense",
    "Palencia",
    "Las Palmas",
    "Pontevedra",
    "La Rioja",
    "Salamanca",
    "Santa Cruz de Tenerife",
    "Segovia",
    "Sevilla",
    "Soria",
    "Tarragona",
    "Teruel",
    "Toledo",
    "València",
    "Valladolid",
    "Zamora",
    "Zaragoza",
]


def set_filters(dfall, news):
    st.sidebar.title("Filtro respuestas")

    filt = pd.Series([True] * dfall.shape[0])

    st.sidebar.header("Noticias")
    news_fake_filt_crit = st.sidebar.multiselect(
        "Escoge las fake que quieras filtrar",
        news[news["is_fake"] == True]["min_title"].values,
        [],
        help="Para omitir el filtro no seleccionar ninguna opción",
    )
    news_fake_filt_crit = news[news["min_title"].isin(news_fake_filt_crit)][
        "news_id"
    ].values
    if len(news_fake_filt_crit) > 0:
        news_fake_filt = dfall["fake_news_id"].isin(news_fake_filt_crit)
        filt &= news_fake_filt

    news_true_filt_crit = st.sidebar.multiselect(
        "Escoge las verdaderas que quieras filtrar",
        news["min_title"].values,
        [],
        help="Para omitir el filtro no seleccionar ninguna opción",
    )
    news_true_filt_crit = news[news["min_title"].isin(news_true_filt_crit)][
        "news_id"
    ].values
    if len(news_true_filt_crit) > 0:
        news_true_filt = dfall["true_news_id"].isin(news_true_filt_crit)
        filt &= news_true_filt

    news_topic_1_filt_crit = st.sidebar.multiselect(
        "Escoge los tópicos 1 que quieras filtrar",
        list(set(news["topic_1"].values)),
        [],
        help="Para omitir el filtro no seleccionar ninguna opción",
    )
    if len(news_topic_1_filt_crit) > 0:
        topic_1_filt = dfall["fake_topic_1"].isin(news_topic_1_filt_crit) | dfall[
            "true_topic_1"
        ].isin(news_topic_1_filt_crit)
        filt &= topic_1_filt

    news_topic_2_filt_crit = st.sidebar.multiselect(
        "Escoge los tópicos 2 que quieras filtrar",
        set(news["topic_2"].values),
        [],
        help="Para omitir el filtro no seleccionar ninguna opción",
    )
    if len(news_topic_2_filt_crit) > 0:
        topic_2_filt = dfall["fake_topic_2"].isin(news_topic_2_filt_crit) | dfall[
            "true_topic_2"
        ].isin(news_topic_2_filt_crit)
        filt &= topic_2_filt

    st.sidebar.header("Percepción")
    grupos_percepcion = [
        "Acierto en la verdadera",
        "Acierto en la falsa",
        "Error en la verdadera",
        "Error en la falsa",
    ]
    grupos_percep_filt_crit = st.sidebar.multiselect(
        "Escoge el grupo por el que quieras filtrar",
        grupos_percepcion,
        [],
        help="Para omitir el filtro no seleccionar ninguna opción",
    )
    if len(grupos_percep_filt_crit) > 0:
        if "Acierto en la verdadera" in grupos_percep_filt_crit:
            perce_true_correct_filt = dfall["tysno_verdadera"] == "sí"
            filt &= perce_true_correct_filt
        if "Acierto en la falsa" in grupos_percep_filt_crit:
            perce_fake_correct_filt = dfall["fysno_verdadera"] == "no"
            filt &= perce_fake_correct_filt
        if "Error en la verdadera" in grupos_percep_filt_crit:
            perce_true_error_filt = dfall["tysno_verdadera"] == "no"
            filt &= perce_true_error_filt
        if "Error en la falsa" in grupos_percep_filt_crit:
            perce_fake_error_filt = dfall["fysno_verdadera"] == "sí"
            filt &= perce_fake_error_filt

    st.sidebar.markdown("***")
    # news_topic_filt
    # grupos_percep_filt

    st.sidebar.title("Filtro demografia")

    st.sidebar.header("Edad")
    demo_age_filt_crit = st.sidebar.multiselect(
        "Escoge las edades a filtrar",
        val_edad,
        [],
        help="Para omitir el filtro no seleccionar ninguna opción",
    )
    if len(demo_age_filt_crit) > 0:
        demo_age_filt = dfall["dm_edad"].isin(demo_age_filt_crit)
        filt &= demo_age_filt

    st.sidebar.header("Género")
    genero = ["Femenino", "Masculino", "No binario", "NS/NC"]
    demo_gen_filt_crit = st.sidebar.multiselect(
        "Escoge el género a filtrar",
        val_genero,
        [],
        help="Para omitir el filtro no seleccionar ninguna opción",
    )
    if len(demo_gen_filt_crit) > 0:
        demo_gen_filt = dfall["dm_genero"].isin(demo_gen_filt_crit)
        filt &= demo_gen_filt

    st.sidebar.header("Estudios")
    demo_edu_filt_crit = st.sidebar.multiselect(
        "Escoge nivel de estudios a filtrar",
        val_estudios,
        [],
        help="Para omitir el filtro no seleccionar ninguna opción",
    )
    if len(demo_edu_filt_crit) > 0:
        demo_edu_filt = dfall["dm_educacion"].isin(demo_edu_filt_crit)
        filt &= demo_edu_filt

    st.sidebar.header("Tecnologia")
    demo_tec_filt_crit = st.sidebar.multiselect(
        "Escoge nivel de estudios a filtrar",
        val_tecno,
        [],
        help="Para omitir el filtro no seleccionar ninguna opción",
    )
    if len(demo_tec_filt_crit) > 0:
        demo_tec_filt = dfall["dm_tecnologia"].isin(demo_tec_filt_crit)
        filt &= demo_tec_filt

    st.sidebar.header("Profesional")
    demo_pro_filt_crit = st.sidebar.multiselect(
        "Escoge ámbito profesional a filtrar",
        val_professional,
        [],
        help="Para omitir el filtro no seleccionar ninguna opción",
    )
    if len(demo_pro_filt_crit) > 0:
        demo_pro_filt = dfall["dm_professional"].isin(demo_pro_filt_crit)
        filt &= demo_pro_filt

    st.sidebar.header("Empleo")
    demo_empleo_filt_crit = st.sidebar.multiselect(
        "Escoge estado laboral a filtrar",
        val_empleo,
        [],
        help="Para omitir el filtro no seleccionar ninguna opción",
    )
    if len(demo_empleo_filt_crit) > 0:
        demo_empleo_filt = dfall["dm_empleo"].isin(demo_empleo_filt_crit)
        filt &= demo_empleo_filt

    st.sidebar.header("Política")
    demo_pol_filt_crit = st.sidebar.multiselect(
        "Escoge orientación política a filtrar",
        val_politica,
        [],
        help="Para omitir el filtro no seleccionar ninguna opción",
    )
    if len(demo_pol_filt_crit) > 0:
        demo_pol_filt = dfall["dm_politica"].isin(demo_pol_filt_crit)
        filt &= demo_pol_filt

    st.sidebar.header("Religión")
    demo_rel_filt_crit = st.sidebar.multiselect(
        "Escoge religión a filtrar",
        val_religion,
        [],
        help="Para omitir el filtro no seleccionar ninguna opción",
    )
    if len(demo_rel_filt_crit) > 0:
        demo_rel_filt = dfall["dm_religion"].isin(demo_rel_filt_crit)
        filt &= demo_rel_filt

    st.sidebar.header("Província")
    demo_prov_filt_crit = st.sidebar.multiselect(
        "Escoge província a filtrar",
        val_provincia,
        [],
        help="Para omitir el filtro no seleccionar ninguna opción",
    )
    if len(demo_prov_filt_crit) > 0:
        demo_prov_filt = dfall["dm_provincia"].isin(demo_prov_filt_crit)
        filt &= demo_prov_filt

    return filt


filt = set_filters(df_all, notis_df)
df_filt = df_all[filt].copy()


st.title("RRSSalud / Resultados experimento")

sections = [
    "Ninguna",
    "Explorar dataset",
    "Comportamiento en plataforma",
    "Análisis descriptivo",
    "Análisis de percepción",
    "Correlaciones",
]
section = st.selectbox("Qué sección quiere ver?", sections)

if section == "Explorar dataset":
    st.header(section)
    st.dataframe(df_filt)

    st.text("Numero de registros: " + str(df_filt.shape[0]))

    st.text("Description categorical variables")
    st.dataframe(df_filt.describe(exclude=[np.number], datetime_is_numeric=True))

    if st.button("Mostrar variables"):
        vars = list(df_filt.columns)
        st.text(f"Hay {len(vars)} variables:")
        for idx, var in enumerate(vars):
            st.text(f"{idx + 1}. {var}")

elif section == "Comportamiento en plataforma":
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

    st.header("Tiempo del experimento")

    st.text(
        "Estadisticas descriptivas de tiempo de completitud del experimento (minutos)\n"
    )
    # df[df['time_completion_min']<=20]['time_completion_min'].plot.hist()
    fig_time_exp, axs = plt.subplots(1, 2, figsize=(15, 5))
    axs[0].hist(df_filt[df_filt["time_completion_min"] <= 20]["time_completion_min"])
    axs[0].title.set_text("Filtered answers")
    plt.figtext(
        0.35,
        0.55,
        df_filt[df_filt["time_completion_min"] <= 20]["time_completion_min"]
        .describe()
        .to_string(),
    )
    axs[1].hist(df_all[df_all["time_completion_min"] <= 20]["time_completion_min"])
    axs[1].title.set_text("All answers")
    plt.figtext(
        0.77,
        0.55,
        df_all[df_all["time_completion_min"] <= 20]["time_completion_min"]
        .describe()
        .to_string(),
    )
    st.pyplot(fig_time_exp)

    st.text(
        "Estadisticas descriptivas de tiempo de lectura de las noticias (segundos)\n"
    )
    fig_time_news, axs = plt.subplots(1, 2, figsize=(15, 5))
    axs[0].hist(df_all[df_all["time_news1"] <= 700]["time_news1"])
    axs[0].title.set_text("News 1")
    plt.figtext(
        0.35,
        0.55,
        df_all[df_all["time_news1"] <= 700]["time_news1"].describe().to_string(),
    )
    axs[1].hist(df_all[df_all["time_news2"] <= 700]["time_news2"])
    axs[1].title.set_text("News 2")
    plt.figtext(
        0.77,
        0.55,
        df_all[df_all["time_news2"] <= 700]["time_news2"].describe().to_string(),
    )
    st.pyplot(fig_time_news)

    st.text(
        "Estadisticas descriptivas de tiempo de lectura de las noticias (segundos)\n"
    )
    fig_time_news_veracity, axs = plt.subplots(1, 2, figsize=(15, 5))

    ft = df_all[df_all["first_true"]][["time_news1", "time_news2"]]
    ft.columns = ["true", "fake"]
    ff = df_all[~df_all["first_true"]][["time_news1", "time_news2"]]
    ff.columns = ["fake", "true"]
    time_true = pd.concat([ft[["true"]], ff[["true"]]])
    time_fake = pd.concat([ft[["fake"]], ff[["fake"]]])

    axs[0].hist(time_true[time_true["true"] <= 700]["true"])
    axs[0].title.set_text("True News")
    plt.figtext(
        0.35, 0.55, time_true[time_true["true"] <= 700]["true"].describe().to_string()
    )

    axs[1].hist(time_fake[time_fake["fake"] <= 700]["fake"])
    axs[1].title.set_text("Fake News")
    plt.figtext(
        0.77, 0.55, time_fake[time_fake["fake"] <= 700]["fake"].describe().to_string()
    )
    st.pyplot(fig_time_news_veracity)

    st.text(
        "Estadisticas descriptivas de tiempo de lectura de las noticias (segundos)\n"
    )
    fig_time_news_4, axs = plt.subplots(2, 2, figsize=(15, 10))

    ft = df_all[df_all["first_true"]][["time_news1", "time_news2"]]
    ft.columns = ["true", "fake"]
    ff = df_all[~df_all["first_true"]][["time_news1", "time_news2"]]
    ff.columns = ["fake", "true"]
    time_true = pd.concat([ft[["true"]], ff[["true"]]])
    time_fake = pd.concat([ft[["fake"]], ff[["fake"]]])

    axs[0][0].hist(ft[ft["true"] <= 700]["true"])
    axs[0][0].title.set_text("First News / True")
    plt.figtext(0.35, 0.7, ft[ft["true"] <= 700]["true"].describe().to_string())

    axs[0][1].hist(ff[ff["true"] <= 700]["true"])
    axs[0][1].title.set_text("Second News / True")
    plt.figtext(0.77, 0.7, ff[ff["true"] <= 700]["true"].describe().to_string())

    axs[1][0].hist(ff[ff["fake"] <= 700]["fake"])
    axs[1][0].title.set_text("First News / Fake")
    plt.figtext(0.35, 0.3, ff[ff["fake"] <= 700]["fake"].describe().to_string())

    axs[1][1].hist(ft[ft["fake"] <= 700]["fake"])
    axs[1][1].title.set_text("Second News / Fake")
    plt.figtext(0.77, 0.3, ft[ft["fake"] <= 700]["fake"].describe().to_string())
    st.pyplot(fig_time_news_4)

    st.header("Adjudicación y sensibilidad a noticias")

    true_freq = pd.concat(
        [
            df_all["true_news"]
            .value_counts(normalize=True)
            .mul(100)
            .round(1)
            .astype(str)
            + "%",
            df_init["true_news"]
            .value_counts(normalize=True)
            .mul(100)
            .round(1)
            .astype(str)
            + "%",
            df["true_news"].value_counts(normalize=True).mul(100).round(1).astype(str)
            + "%",
        ],
        axis=1,
    )
    true_freq.columns = ["Adjudicadas", "Inicializadas", "Finalizadas"]

    fake_freq = pd.concat(
        [
            df_all["fake_news"]
            .value_counts(normalize=True)
            .mul(100)
            .round(1)
            .astype(str)
            + "%",
            df_init["fake_news"]
            .value_counts(normalize=True)
            .mul(100)
            .round(1)
            .astype(str)
            + "%",
            df["fake_news"].value_counts(normalize=True).mul(100).round(1).astype(str)
            + "%",
        ],
        axis=1,
    )
    fake_freq.columns = ["Adjudicadas", "Inicializadas", "Finalizadas"]

    st.text("Frecuencia adjudicación noticias verdaderas")
    st.dataframe(true_freq[["Inicializadas", "Finalizadas"]])

    st.text("Frecuencia adjudicación noticias falsas")
    st.dataframe(fake_freq[["Adjudicadas", "Finalizadas"]])

    st.text("Probabilidad de finalización del experimento dada una noticia verdadera")
    true_freq_abs = pd.concat(
        [df_init["true_news"].value_counts(), df["true_news"].value_counts()], axis=1
    )
    true_freq_abs.columns = ["init", "fin"]
    true_freq_abs["prob_fin"] = true_freq_abs["fin"] / true_freq_abs["init"]
    true_freq_abs.sort_values("prob_fin", ascending=False)["prob_fin"].mul(100).round(
        1
    ).astype(str) + "%"

    st.text("Probabilidad de finalización del experimento dada una noticia falsa")
    fake_freq_abs = pd.concat(
        [df_init["fake_news"].value_counts(), df["fake_news"].value_counts()], axis=1
    )
    fake_freq_abs.columns = ["init", "fin"]
    fake_freq_abs["prob_fin"] = fake_freq_abs["fin"] / fake_freq_abs["init"]
    fake_freq_abs.sort_values("prob_fin", ascending=False)["prob_fin"].mul(100).round(
        1
    ).astype(str) + "%"


elif section == "Análisis descriptivo":
    st.header(section)

    st.header("Demográfico")

    st.text("Distribución de " + "dm_edad")
    fig = plt.figure(figsize=(15, 5))
    plt.subplot(1, 2, 1)
    ax = df_filt["dm_edad"].value_counts().reindex(val_edad).plot.bar()
    # ax.set_xlabel('dm_edad', fontsize=13)
    ax.set_ylabel("Frecuencia", fontsize=13)
    ax.title.set_text("Filtered answers")
    for p in ax.patches:
        h_col = int(p.get_height())
        ax.annotate(
            f"{h_col} ({round(100 * (h_col / df_filt.shape[0]), 1)}%)",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            fontsize=12,
            color="black",
            xytext=(0, 10),
            textcoords="offset points",
        )
    plt.subplot(1, 2, 2)
    ax = df_all["dm_edad"].value_counts().reindex(val_edad).plot.bar()
    # ax.set_xlabel('dm_edad', fontsize=13)
    ax.set_ylabel("Frecuencia", fontsize=13)
    ax.title.set_text("All answers")
    for p in ax.patches:
        h_col = int(p.get_height())
        ax.annotate(
            f"{h_col} ({round(100 * (h_col / df_all.shape[0]), 1)}%)",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            fontsize=12,
            color="black",
            xytext=(0, 10),
            textcoords="offset points",
        )
    st.pyplot(fig)

    st.text("Distribución de " + "dm_genero")
    fig = plt.figure(figsize=(15, 5))
    plt.subplot(1, 2, 1)
    ax = df_filt["dm_genero"].value_counts().reindex(val_genero).plot.bar()
    # ax.set_xlabel('dm_genero', fontsize=13)
    ax.set_ylabel("Frecuencia", fontsize=13)
    ax.title.set_text("Filtered answers")
    for p in ax.patches:
        h_col = int(p.get_height())
        ax.annotate(
            f"{h_col} ({round(100 * (h_col / df_filt.shape[0]), 1)}%)",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            fontsize=12,
            color="black",
            xytext=(0, 10),
            textcoords="offset points",
        )
    plt.subplot(1, 2, 2)
    ax = df_all["dm_genero"].value_counts().reindex(val_genero).plot.bar()
    # ax.set_xlabel('dm_genero', fontsize=13)
    ax.set_ylabel("Frecuencia", fontsize=13)
    ax.title.set_text("All answers")
    for p in ax.patches:
        h_col = int(p.get_height())
        ax.annotate(
            f"{h_col} ({round(100 * (h_col / df_all.shape[0]), 1)}%)",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            fontsize=12,
            color="black",
            xytext=(0, 10),
            textcoords="offset points",
        )
    st.pyplot(fig)

    st.text("Distribución de " + "dm_educacion")
    fig = plt.figure(figsize=(15, 5))
    plt.subplot(1, 2, 1)
    ax = df_filt["dm_educacion"].value_counts().reindex(val_estudios).plot.bar()
    # ax.set_xlabel('dm_educacion', fontsize=13)
    ax.set_ylabel("Frecuencia", fontsize=13)
    ax.title.set_text("Filtered answers")
    for p in ax.patches:
        h_col = int(p.get_height())
        ax.annotate(
            f"{h_col} ({round(100 * (h_col / df_filt.shape[0]), 1)}%)",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            fontsize=12,
            color="black",
            xytext=(0, 10),
            textcoords="offset points",
        )
    plt.subplot(1, 2, 2)
    ax = df_all["dm_educacion"].value_counts().reindex(val_estudios).plot.bar()
    # ax.set_xlabel('dm_educacion', fontsize=13)
    ax.set_ylabel("Frecuencia", fontsize=13)
    ax.title.set_text("All answers")
    for p in ax.patches:
        h_col = int(p.get_height())
        ax.annotate(
            f"{h_col} ({round(100 * (h_col / df_all.shape[0]), 1)}%)",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            fontsize=12,
            color="black",
            xytext=(0, 10),
            textcoords="offset points",
        )
    st.pyplot(fig)

    st.text("Distribución de " + "dm_tecnologia")
    fig = plt.figure(figsize=(15, 5))
    plt.subplot(1, 2, 1)
    ax = df_filt["dm_tecnologia"].value_counts().reindex(val_tecno).plot.bar()
    # ax.set_xlabel('dm_tecnologia', fontsize=13)
    ax.set_ylabel("Frecuencia", fontsize=13)
    ax.title.set_text("Filtered answers")
    for p in ax.patches:
        h_col = int(p.get_height())
        ax.annotate(
            f"{h_col} ({round(100 * (h_col / df_filt.shape[0]), 1)}%)",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            fontsize=12,
            color="black",
            xytext=(0, 10),
            textcoords="offset points",
        )
    plt.subplot(1, 2, 2)
    ax = df_all["dm_tecnologia"].value_counts().reindex(val_tecno).plot.bar()
    # ax.set_xlabel('dm_tecnologia', fontsize=13)
    ax.set_ylabel("Frecuencia", fontsize=13)
    ax.title.set_text("All answers")
    for p in ax.patches:
        h_col = int(p.get_height())
        ax.annotate(
            f"{h_col} ({round(100 * (h_col / df_all.shape[0]), 1)}%)",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            fontsize=12,
            color="black",
            xytext=(0, 10),
            textcoords="offset points",
        )
    st.pyplot(fig)

    st.text("Distribución de " + "dm_empleo")
    fig = plt.figure(figsize=(15, 5))
    plt.subplot(1, 2, 1)
    ax = df_filt["dm_empleo"].value_counts().reindex(val_empleo).plot.bar()
    # ax.set_xlabel('dm_empleo', fontsize=13)
    ax.set_ylabel("Frecuencia", fontsize=13)
    ax.title.set_text("Filtered answers")
    for p in ax.patches:
        h_col = int(p.get_height())
        ax.annotate(
            f"{h_col} ({round(100 * (h_col / df_filt.shape[0]), 1)}%)",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            fontsize=12,
            color="black",
            xytext=(0, 10),
            textcoords="offset points",
        )
    plt.subplot(1, 2, 2)
    ax = df_all["dm_empleo"].value_counts().reindex(val_empleo).plot.bar()
    # ax.set_xlabel('dm_empleo', fontsize=13)
    ax.set_ylabel("Frecuencia", fontsize=13)
    ax.title.set_text("All answers")
    for p in ax.patches:
        h_col = int(p.get_height())
        ax.annotate(
            f"{h_col} ({round(100 * (h_col / df_all.shape[0]), 1)}%)",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            fontsize=12,
            color="black",
            xytext=(0, 10),
            textcoords="offset points",
        )
    st.pyplot(fig)

    st.text("Distribución de " + "dm_politica")
    fig = plt.figure(figsize=(15, 5))
    plt.subplot(1, 2, 1)
    ax = df_filt["dm_politica"].value_counts().reindex(val_politica).plot.bar()
    # ax.set_xlabel('dm_politica', fontsize=13)
    ax.set_ylabel("Frecuencia", fontsize=13)
    ax.title.set_text("Filtered answers")
    for p in ax.patches:
        h_col = int(p.get_height())
        ax.annotate(
            f"{h_col} ({round(100 * (h_col / df_filt.shape[0]), 1)}%)",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            fontsize=12,
            color="black",
            xytext=(0, 10),
            textcoords="offset points",
        )
    plt.subplot(1, 2, 2)
    ax = df_all["dm_politica"].value_counts().reindex(val_politica).plot.bar()
    # ax.set_xlabel('dm_politica', fontsize=13)
    ax.set_ylabel("Frecuencia", fontsize=13)
    ax.title.set_text("All answers")
    for p in ax.patches:
        h_col = int(p.get_height())
        ax.annotate(
            f"{h_col} ({round(100 * (h_col / df_all.shape[0]), 1)}%)",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            fontsize=12,
            color="black",
            xytext=(0, 10),
            textcoords="offset points",
        )
    st.pyplot(fig)

    st.text("Distribución de " + "dm_religion")
    fig = plt.figure(figsize=(15, 5))
    plt.subplot(1, 2, 1)
    ax = df_filt["dm_religion"].value_counts().reindex(val_religion).plot.bar()
    # ax.set_xlabel('dm_religion', fontsize=13)
    ax.set_ylabel("Frecuencia", fontsize=13)
    ax.title.set_text("Filtered answers")
    for p in ax.patches:
        h_col = int(p.get_height())
        ax.annotate(
            f"{h_col} ({round(100 * (h_col / df_filt.shape[0]), 1)}%)",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            fontsize=12,
            color="black",
            xytext=(0, 10),
            textcoords="offset points",
        )
    plt.subplot(1, 2, 2)
    ax = df_all["dm_religion"].value_counts().reindex(val_religion).plot.bar()
    # ax.set_xlabel('dm_religion', fontsize=13)
    ax.set_ylabel("Frecuencia", fontsize=13)
    ax.title.set_text("All answers")
    for p in ax.patches:
        h_col = int(p.get_height())
        ax.annotate(
            f"{h_col} ({round(100 * (h_col / df_all.shape[0]), 1)}%)",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            fontsize=12,
            color="black",
            xytext=(0, 10),
            textcoords="offset points",
        )
    st.pyplot(fig)

    st.text("Distribución dm_professional")
    fig, ax = plt.subplots()
    var = "dm_professional"
    x_label = "Profesión"
    y_label = "Frecuencia"
    ax = (
        df_all[var]
        .value_counts()
        .sort_values(ascending=True)
        .plot.barh(figsize=(16, 12))
    )
    ax.set_xlabel(x_label, fontsize=13)
    ax.set_ylabel(y_label, fontsize=13)
    ax.title.set_text("All answers")
    plt.xticks(size=12)
    plt.yticks(size=12)
    plt.grid(False, which="major", axis="x")
    for p in ax.patches:
        w_col = int(p.get_width())
        ax.annotate(
            f"{w_col} ({round(100 * (w_col / df_all.shape[0]), 1)}%)",
            (p.get_x() + p.get_width() + 2.8, p.get_y() - 0.5),
            ha="center",
            va="center",
            fontsize=12,
            color="black",
            xytext=(0, 10),
            textcoords="offset points",
        )
    st.pyplot(fig)

    st.text("Distribución de residencia")
    fig, ax = plt.subplots()
    var = "dm_lugar"
    x_label = "Lugar"
    y_label = "Frecuencia"
    ax = (
        df_all[var]
        .value_counts()
        .sort_values(ascending=True)
        .plot.barh(figsize=(16, 12))
    )
    ax.set_xlabel(x_label, fontsize=13)
    ax.set_ylabel(y_label, fontsize=13)
    ax.title.set_text("All answers")
    plt.xticks(size=12)
    plt.yticks(size=12)
    plt.grid(False, which="major", axis="x")
    for p in ax.patches:
        w_col = int(p.get_width())
        ax.annotate(
            f"{w_col} ({round(100 * (w_col / df_all.shape[0]), 1)}%)",
            (p.get_x() + p.get_width() + 2.8, p.get_y() - 0.5),
            ha="center",
            va="center",
            fontsize=12,
            color="black",
            xytext=(0, 10),
            textcoords="offset points",
        )
    st.pyplot(fig)

    st.header("Hábitos informativos (all answers)")
    # Prepare data
    category_names = [
        "Diario",
        "Algunas veces en la semana",
        "Algunas veces al mes",
        "Algunas veces en los últimos 12 meses",
        "Nunca",
        "NS/NC",
    ]
    results = dict()
    for var in vars_routine:
        key = var.split("_")[1].title()
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
        category_colors = plt.get_cmap("RdYlGn")(np.linspace(0.15, 0.85, data.shape[1]))

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.invert_yaxis()
        ax.xaxis.set_visible(False)
        ax.set_xlim(0, np.sum(data, axis=1).max())

        for i, (colname, color) in enumerate(zip(category_names, category_colors)):
            widths = data[:, i]
            starts = data_cum[:, i] - widths
            ax.barh(labels, widths, left=starts, height=0.5, label=colname, color=color)
            xcenters = starts + widths / 2

            r, g, b, _ = color
            text_color = "white" if r * g * b < 0.5 else "darkgrey"
            for y, (x, c) in enumerate(zip(xcenters, widths)):
                if int(c) == 0:
                    continue
                ax.text(
                    x, y, f"{str(int(c))}", ha="center", va="center", color=text_color
                )
        ax.legend(
            ncol=len(category_names),
            bbox_to_anchor=(0, 1),
            loc="lower left",
            fontsize="small",
        )

        return fig, ax

    fig, ax = routine_responses(results, category_names)
    st.pyplot(fig)


elif section == "Análisis de percepción":
    st.header(section)

    st.header("Percepción vericidad")

    st.markdown("Respuesta sobre noticia **`falsa`** adjudicada")
    fig = plt.figure(figsize=(15, 5))
    plt.subplot(1, 2, 1)
    ax = df_filt["fysno_verdadera"].value_counts().reindex(["sí", "no"]).plot.bar()
    ax.set_xlabel("¿Cree que es verdadera la noticia [falsa]?", fontsize=13)
    ax.set_ylabel("Frecuencia", fontsize=13)
    ax.title.set_text("Filtered answers")
    plt.xticks(size=12, rotation=0)
    plt.yticks(size=12)
    plt.grid(False, which="major", axis="x")
    for p in ax.patches:
        h_col = int(p.get_height())
        div_num = df_filt.shape[0]
        if div_num == 0:
            div_num = 1
        ax.annotate(
            f"{h_col} ({round(100 * (h_col / div_num), 1)}%)",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            fontsize=12,
            color="black",
            xytext=(0, 10),
            textcoords="offset points",
        )
    plt.subplot(1, 2, 2)
    ax = df_all["fysno_verdadera"].value_counts().reindex(["sí", "no"]).plot.bar()
    ax.set_xlabel("¿Cree que es verdadera la noticia [falsa]?", fontsize=13)
    ax.set_ylabel("Frecuencia", fontsize=13)
    ax.title.set_text("All answers")
    plt.xticks(size=12, rotation=0)
    plt.yticks(size=12)
    plt.grid(False, which="major", axis="x")
    for p in ax.patches:
        h_col = int(p.get_height())
        ax.annotate(
            f"{h_col} ({round(100 * (h_col / df_all.shape[0]), 1)}%)",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            fontsize=12,
            color="black",
            xytext=(0, 10),
            textcoords="offset points",
        )
    st.pyplot(fig)

    st.markdown("Noticias **`falsas`** ordenadas por errores en detección ")

    fake_news_names = list(df_filt["fake_news"].unique())
    rights, rights_str, wrongs, wrongs_str = [], [], [], []
    for name in fake_news_names:
        div_num = df_filt.loc[df_filt["fake_news"] == name, :].shape[0]
        if div_num == 0:
            div_num = 1
        errors = (
            df_filt.loc[
                (df_filt["fake_news"] == name) & (df_filt["fysno_verdadera"] == "sí"), :
            ].shape[0]
            / div_num
        )
        no_errors = (
            df_filt.loc[
                (df_filt["fake_news"] == name) & (df_filt["fysno_verdadera"] == "no"), :
            ].shape[0]
            / div_num
        )
        wrongs.append(round(errors * 100, 1))
        wrongs_str.append(str(round(errors * 100, 1)) + "%")
        rights.append(round(no_errors * 100, 1))
        rights_str.append(str(round(no_errors * 100, 1)) + "%")
    fake_news_df_filt = pd.DataFrame.from_dict(
        {
            "Noticia falsa": fake_news_names,
            "Marcada como verdadera (Error)": wrongs_str,
            "Marcada como falsa (Acierto)": rights_str,
            "wrong": wrongs,
            "rights": rights,
        }
    )
    fake_news_df_filt.sort_values(
        by="wrong", ascending=False, ignore_index=True, inplace=True
    )

    fake_news_names = list(df_all["fake_news"].unique())
    rights, rights_str, wrongs, wrongs_str = [], [], [], []
    for name in fake_news_names:
        div_num = df_all.loc[df_all["fake_news"] == name, :].shape[0]
        if div_num == 0:
            div_num = 1
        errors = (
            df_all.loc[
                (df_all["fake_news"] == name) & (df_all["fysno_verdadera"] == "sí"), :
            ].shape[0]
            / div_num
        )
        no_errors = (
            df_all.loc[
                (df_all["fake_news"] == name) & (df_all["fysno_verdadera"] == "no"), :
            ].shape[0]
            / div_num
        )
        wrongs.append(round(errors * 100, 1))
        wrongs_str.append(str(round(errors * 100, 1)) + "%")
        rights.append(round(no_errors * 100, 1))
        rights_str.append(str(round(no_errors * 100, 1)) + "%")
    fake_news_df_all = pd.DataFrame.from_dict(
        {
            "Noticia falsa": fake_news_names,
            "Marcada como verdadera (Error)": wrongs_str,
            "Marcada como falsa (Acierto)": rights_str,
            "wrong": wrongs,
            "rights": rights,
        }
    )
    fake_news_df_all.sort_values(
        by="wrong", ascending=False, ignore_index=True, inplace=True
    )

    col1, col2 = st.beta_columns(2)
    col1.subheader("Filtered news")
    col1.dataframe(
        fake_news_df_filt[
            [
                "Noticia falsa",
                "Marcada como verdadera (Error)",
                "Marcada como falsa (Acierto)",
            ]
        ]
    )
    col2.subheader("All news")
    col2.dataframe(
        fake_news_df_all[
            [
                "Noticia falsa",
                "Marcada como verdadera (Error)",
                "Marcada como falsa (Acierto)",
            ]
        ]
    )

    st.markdown("Respuesta sobre noticia **`verdadera`** adjudicada")
    fig = plt.figure(figsize=(15, 5))
    plt.subplot(1, 2, 1)
    ax = df_filt["tysno_verdadera"].value_counts().reindex(["sí", "no"]).plot.bar()
    ax.set_xlabel("¿Cree que es verdadera la noticia [verdadera]?", fontsize=13)
    ax.set_ylabel("Frecuencia", fontsize=13)
    ax.title.set_text("Filtered answers")
    plt.xticks(size=12, rotation=0)
    plt.yticks(size=12)
    plt.grid(False, which="major", axis="x")
    for p in ax.patches:
        h_col = int(p.get_height())
        div_num = df_filt.shape[0]
        if div_num == 0:
            div_num = 1
        ax.annotate(
            f"{h_col} ({round(100 * (h_col / div_num), 1)}%)",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            fontsize=12,
            color="black",
            xytext=(0, 10),
            textcoords="offset points",
        )
    plt.subplot(1, 2, 2)
    ax = df_all["tysno_verdadera"].value_counts().reindex(["sí", "no"]).plot.bar()
    ax.set_xlabel("¿Cree que es verdadera la noticia [verdadera]?", fontsize=13)
    ax.set_ylabel("Frecuencia", fontsize=13)
    ax.title.set_text("All answers")
    plt.xticks(size=12, rotation=0)
    plt.yticks(size=12)
    plt.grid(False, which="major", axis="x")
    for p in ax.patches:
        h_col = int(p.get_height())
        div_num = df_all.shape[0]
        if div_num == 0:
            div_num = 1
        ax.annotate(
            f"{h_col} ({round(100 * (h_col / div_num), 1)}%)",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            fontsize=12,
            color="black",
            xytext=(0, 10),
            textcoords="offset points",
        )
    st.pyplot(fig)

    st.markdown("Noticias **`verdaderas`** ordenadas por errores en detección ")
    news_names = list(df_filt["true_news"].unique())
    rights, rights_str, wrongs, wrongs_str = [], [], [], []
    for name in news_names:
        div_num = df_filt.loc[df_filt["true_news"] == name, :].shape[0]
        if div_num == 0:
            div_num = 1
        errors = (
            df_filt.loc[
                (df_filt["true_news"] == name) & (df_filt["tysno_verdadera"] == "no"), :
            ].shape[0]
            / div_num
        )
        no_errors = (
            df_filt.loc[
                (df_filt["true_news"] == name) & (df_filt["tysno_verdadera"] == "sí"), :
            ].shape[0]
            / div_num
        )
        wrongs.append(round(errors * 100, 1))
        wrongs_str.append(str(round(errors * 100, 1)) + "%")
        rights.append(round(no_errors * 100, 1))
        rights_str.append(str(round(no_errors * 100, 1)) + "%")
    news_df_filt = pd.DataFrame.from_dict(
        {
            "Noticia verdadera": news_names,
            "Marcada como falsa (Error)": wrongs_str,
            "Marcada como verdadera (Acierto)": rights_str,
            "wrong": wrongs,
            "rights": rights,
        }
    )
    news_df_filt.sort_values(
        by="wrong", ascending=False, ignore_index=True, inplace=True
    )

    news_names = list(df_all["true_news"].unique())
    rights, rights_str, wrongs, wrongs_str = [], [], [], []
    for name in news_names:
        div_num = df_all.loc[df_all["true_news"] == name, :].shape[0]
        if div_num == 0:
            div_num = 1
        errors = (
            df_all.loc[
                (df_all["true_news"] == name) & (df_all["tysno_verdadera"] == "no"), :
            ].shape[0]
            / div_num
        )
        no_errors = (
            df_all.loc[
                (df_all["true_news"] == name) & (df_all["tysno_verdadera"] == "sí"), :
            ].shape[0]
            / div_num
        )
        wrongs.append(round(errors * 100, 1))
        wrongs_str.append(str(round(errors * 100, 1)) + "%")
        rights.append(round(no_errors * 100, 1))
        rights_str.append(str(round(no_errors * 100, 1)) + "%")
    news_df_all = pd.DataFrame.from_dict(
        {
            "Noticia verdadera": news_names,
            "Marcada como falsa (Error)": wrongs_str,
            "Marcada como verdadera (Acierto)": rights_str,
            "wrong": wrongs,
            "rights": rights,
        }
    )
    news_df_all.sort_values(
        by="wrong", ascending=False, ignore_index=True, inplace=True
    )

    col1, col2 = st.beta_columns(2)
    col1.subheader("Filtered news")
    col1.dataframe(
        news_df_filt[
            [
                "Noticia verdadera",
                "Marcada como falsa (Error)",
                "Marcada como verdadera (Acierto)",
            ]
        ]
    )
    col2.subheader("All news")
    col2.dataframe(
        news_df_all[
            [
                "Noticia verdadera",
                "Marcada como falsa (Error)",
                "Marcada como verdadera (Acierto)",
            ]
        ]
    )

    st.header("Análisis de justificaciones")

    st.markdown("***")

    st.markdown(
        "Justificaciones sobre noticias **`falsas`** marcadas como *`verdaderas`*"
    )
    vars_justifications_fake_checked_true = [
        "fys_recuerda_leida",
        "fys_medio_conocido",
        "fys_medio_fiable",
        "fys_fuentes_conocidas",
        "fys_fuentes_confiables",
        "fys_abordaje_serio",
        "fys_coherente",
        "fys_concuerda_creencias",
        "fys_alineado_ideologia",
        "fys_otro",
    ]
    justifications_filt = []
    num_justifications_filt = []
    num_justifications_str_filt = []
    justifications_all = []
    num_justifications_all = []
    num_justifications_str_all = []
    for var in vars_justifications_fake_checked_true:
        justifications_filt.append(" ".join(var.split("_")[1:]))
        div_num = df_filt.loc[df_filt["fysno_verdadera"] == "sí", :].shape[0]
        if div_num == 0:
            div_num = 1
        num_just = round(
            df_filt.loc[
                (df_filt["fysno_verdadera"] == "sí") & (df_filt[var] == "checked"), :
            ].shape[0]
            / div_num
            * 100,
            1,
        )
        num_justifications_filt.append(num_just)
        num_justifications_str_filt.append(str(num_just) + "%")
        justifications_all.append(" ".join(var.split("_")[1:]))
        div_num = df_all.loc[df_all["fysno_verdadera"] == "sí", :].shape[0]
        if div_num == 0:
            div_num = 1
        num_just = round(
            df_all.loc[
                (df_all["fysno_verdadera"] == "sí") & (df_all[var] == "checked"), :
            ].shape[0]
            / div_num
            * 100,
            1,
        )
        num_justifications_all.append(num_just)
        num_justifications_str_all.append(str(num_just) + "%")

    justifications_df_filt = pd.DataFrame.from_dict(
        {
            "Justificacion": justifications_filt,
            "Num. Seleccion": num_justifications_str_filt,
            "num_just": num_justifications_filt,
        }
    )
    justifications_df_filt.sort_values(
        by="num_just", ignore_index=True, inplace=True, ascending=False
    )
    justifications_df_all = pd.DataFrame.from_dict(
        {
            "Justificacion": justifications_all,
            "Num. Seleccion": num_justifications_str_all,
            "num_just": num_justifications_all,
        }
    )
    justifications_df_all.sort_values(
        by="num_just", ignore_index=True, inplace=True, ascending=False
    )

    col1, col2 = st.beta_columns(2)
    col1.subheader("Filtered news")
    col1.dataframe(justifications_df_filt[["Justificacion", "Num. Seleccion"]].head(10))
    col2.subheader("All news")
    col2.dataframe(justifications_df_all[["Justificacion", "Num. Seleccion"]].head(10))

    st.markdown("***")
    st.markdown("Justificaciones sobre noticias **`falsas`** marcadas como *`falsas`*")
    vars_justifications_fake_checked_false = [
        "fno_aclaracion_desmintiendo",
        "fno_medio_desconocido",
        "fno_medio_poco_fiable",
        "fno_fuentes_desconocidas",
        "fno_fuentes_no_confiables",
        "fno_sin_fuentes",
        "fno_abordaje_no_serio",
        "fno_no_coherente",
        "fno_titulo_sensacionalista",
        "fno_imagen_sensacionalista",
        "fno_no_concuerda_creencias",
        "fno_no_alineado_ideologia",
        "fno_otro",
    ]
    justifications_filt = []
    num_justifications_filt = []
    num_justifications_str_filt = []
    justifications_all = []
    num_justifications_all = []
    num_justifications_str_all = []
    for var in vars_justifications_fake_checked_false:
        justifications_filt.append(" ".join(var.split("_")[1:]))
        div_num = df_filt.loc[df_filt["fysno_verdadera"] == "no", :].shape[0]
        if div_num == 0:
            div_num = 1
        num_just = round(
            df_filt.loc[
                (df_filt["fysno_verdadera"] == "no") & (df_filt[var] == "checked"), :
            ].shape[0]
            / div_num
            * 100,
            1,
        )
        num_justifications_filt.append(num_just)
        num_justifications_str_filt.append(str(num_just) + "%")
        justifications_all.append(" ".join(var.split("_")[1:]))
        div_num = df_all.loc[df_all["fysno_verdadera"] == "no", :].shape[0]
        if div_num == 0:
            div_num = 1
        num_just = round(
            df_all.loc[
                (df_all["fysno_verdadera"] == "no") & (df_all[var] == "checked"), :
            ].shape[0]
            / div_num
            * 100,
            1,
        )
        num_justifications_all.append(num_just)
        num_justifications_str_all.append(str(num_just) + "%")
    justifications_df_filt = pd.DataFrame.from_dict(
        {
            "Justificacion": justifications_filt,
            "Num. Seleccion": num_justifications_str_filt,
            "num_just": num_justifications_filt,
        }
    )
    justifications_df_filt.sort_values(
        by="num_just", ignore_index=True, inplace=True, ascending=False
    )
    justifications_df_all = pd.DataFrame.from_dict(
        {
            "Justificacion": justifications_all,
            "Num. Seleccion": num_justifications_str_all,
            "num_just": num_justifications_all,
        }
    )
    justifications_df_all.sort_values(
        by="num_just", ignore_index=True, inplace=True, ascending=False
    )

    col1, col2 = st.beta_columns(2)
    col1.subheader("Filtered news")
    col1.dataframe(justifications_df_filt[["Justificacion", "Num. Seleccion"]].head(10))
    col2.subheader("All news")
    col2.dataframe(justifications_df_all[["Justificacion", "Num. Seleccion"]].head(10))

    st.markdown("***")
    st.markdown(
        "Justificaciones sobre noticias **`verdaderas`** marcadas como *`falsas`*"
    )
    vars_justifications_true_checked_false = [
        "tno_aclaracion_desmintiendo",
        "tno_medio_desconocido",
        "tno_medio_poco_fiable",
        "tno_fuentes_desconocidas",
        "tno_fuentes_no_confiables",
        "tno_sin_fuentes",
        "tno_abordaje_no_serio",
        "tno_no_coherente",
        "tno_titulo_sensacionalista",
        "tno_imagen_sensacionalista",
        "tno_no_concuerda_creencias",
        "tno_no_alineado_ideologia",
        "tno_otro",
    ]
    justifications_filt = []
    num_justifications_filt = []
    num_justifications_str_filt = []
    justifications_all = []
    num_justifications_all = []
    num_justifications_str_all = []
    for var in vars_justifications_true_checked_false:
        justifications_filt.append(" ".join(var.split("_")[1:]))
        div_num = df_filt.loc[df_filt["tysno_verdadera"] == "no", :].shape[0]
        if div_num == 0:
            div_num = 1
        num_just = round(
            df_filt.loc[
                (df_filt["tysno_verdadera"] == "no") & (df_filt[var] == "checked"), :
            ].shape[0]
            / div_num
            * 100,
            1,
        )
        num_justifications_filt.append(num_just)
        num_justifications_str_filt.append(str(num_just) + "%")
        justifications_all.append(" ".join(var.split("_")[1:]))
        div_num = df_all.loc[df_all["tysno_verdadera"] == "no", :].shape[0]
        if div_num == 0:
            div_num = 1
        num_just = round(
            df_all.loc[
                (df_all["tysno_verdadera"] == "no") & (df_all[var] == "checked"), :
            ].shape[0]
            / div_num
            * 100,
            1,
        )
        num_justifications_all.append(num_just)
        num_justifications_str_all.append(str(num_just) + "%")

    justifications_df_filt = pd.DataFrame.from_dict(
        {
            "Justificacion": justifications_filt,
            "Num. Seleccion": num_justifications_str_filt,
            "num_just": num_justifications_filt,
        }
    )
    justifications_df_filt.sort_values(
        by="num_just", ignore_index=True, inplace=True, ascending=False
    )
    justifications_df_all = pd.DataFrame.from_dict(
        {
            "Justificacion": justifications_all,
            "Num. Seleccion": num_justifications_str_all,
            "num_just": num_justifications_all,
        }
    )
    justifications_df_all.sort_values(
        by="num_just", ignore_index=True, inplace=True, ascending=False
    )

    col1, col2 = st.beta_columns(2)
    col1.subheader("Filtered news")
    col1.dataframe(justifications_df_filt[["Justificacion", "Num. Seleccion"]].head(10))
    col2.subheader("All news")
    col2.dataframe(justifications_df_all[["Justificacion", "Num. Seleccion"]].head(10))

    st.markdown("***")
    st.markdown(
        "Justificaciones sobre noticias **`verdaderas`** marcadas como *`verdadera`*"
    )
    vars_justifications_true_checked_true = [
        "tys_recuerda_leida",
        "tys_medio_comunicacion_conocido",
        "tys_medio_comunicacion_fiable",
        "tys_fuentes_conocidas",
        "tys_fuentes_confiables",
        "tys_abordaje_serio",
        "tys_coherente",
        "tys_concuerda_creencias",
        "tys_alineado_ideologia",
        "tys_otro",
    ]
    justifications_filt = []
    num_justifications_filt = []
    num_justifications_str_filt = []
    justifications_all = []
    num_justifications_all = []
    num_justifications_str_all = []
    for var in vars_justifications_true_checked_true:
        justifications_filt.append(" ".join(var.split("_")[1:]))
        div_num = df_filt.loc[df_filt["tysno_verdadera"] == "sí", :].shape[0]
        if div_num == 0:
            div_num = 1
        num_just = round(
            df_filt.loc[
                (df_filt["tysno_verdadera"] == "sí") & (df_filt[var] == "checked"), :
            ].shape[0]
            / div_num
            * 100,
            1,
        )
        num_justifications_filt.append(num_just)
        num_justifications_str_filt.append(str(num_just) + "%")
        justifications_all.append(" ".join(var.split("_")[1:]))
        div_num = df_all.loc[df_all["tysno_verdadera"] == "sí", :].shape[0]
        if div_num == 0:
            div_num = 1
        num_just = round(
            df_all.loc[
                (df_all["tysno_verdadera"] == "sí") & (df_all[var] == "checked"), :
            ].shape[0]
            / div_num
            * 100,
            1,
        )
        num_justifications_all.append(num_just)
        num_justifications_str_all.append(str(num_just) + "%")
    justifications_df_filt = pd.DataFrame.from_dict(
        {
            "Justificacion": justifications_filt,
            "Num. Seleccion": num_justifications_str_filt,
            "num_just": num_justifications_filt,
        }
    )
    justifications_df_filt.sort_values(
        by="num_just", ignore_index=True, inplace=True, ascending=False
    )
    justifications_df_all = pd.DataFrame.from_dict(
        {
            "Justificacion": justifications_all,
            "Num. Seleccion": num_justifications_str_all,
            "num_just": num_justifications_all,
        }
    )
    justifications_df_all.sort_values(
        by="num_just", ignore_index=True, inplace=True, ascending=False
    )

    col1, col2 = st.beta_columns(2)
    col1.subheader("Filtered news")
    col1.dataframe(justifications_df_filt[["Justificacion", "Num. Seleccion"]].head(10))
    col2.subheader("All news")
    col2.dataframe(justifications_df_all[["Justificacion", "Num. Seleccion"]].head(10))

    st.header("Análisis de acciones")

    st.markdown("Acciones en noticias falsas")
    vars_actions_checked_false = [
        "faf_compartira_familia_amigos",
        "faf_publicara_redes",
        "faf_consultara_fuentes",
        "faf_aplicara_aprendido",
        "faf_no_accion",
    ]
    actions_filt = []
    num_actions_filt = []
    num_actions_str_filt = []
    actions_all = []
    num_actions_all = []
    num_actions_str_all = []
    for var in vars_actions_checked_false:
        actions_filt.append(" ".join(var.split("_")[1:]))
        div_num = df_filt.loc[df_filt[var] != "-", :].shape[0]
        if div_num == 0:
            div_num = 1
        num_act = round(
            df_filt.loc[df_filt[var] == "checked", :].shape[0] / div_num * 100, 1
        )
        num_actions_filt.append(num_act)
        num_actions_str_filt.append(str(num_act) + "%")

        actions_all.append(" ".join(var.split("_")[1:]))
        div_num = df_all.loc[df_all[var] != "-", :].shape[0]
        if div_num == 0:
            div_num = 1
        num_act = round(
            df_all.loc[df_all[var] == "checked", :].shape[0] / div_num * 100, 1
        )
        num_actions_all.append(num_act)
        num_actions_str_all.append(str(num_act) + "%")

    actions_df_filt = pd.DataFrame.from_dict(
        {
            "Actions": actions_filt,
            "Num. Seleccion": num_actions_str_filt,
            "num_act": num_actions_filt,
        }
    )
    actions_df_filt.sort_values(
        by="num_act", ignore_index=True, inplace=True, ascending=False
    )
    actions_df_all = pd.DataFrame.from_dict(
        {
            "Actions": actions_all,
            "Num. Seleccion": num_actions_str_all,
            "num_act": num_actions_all,
        }
    )
    actions_df_all.sort_values(
        by="num_act", ignore_index=True, inplace=True, ascending=False
    )

    col1, col2 = st.beta_columns(2)
    col1.subheader("Filtered news")
    col1.dataframe(
        actions_df_filt[["Actions", "Num. Seleccion"]].head(len(actions_filt))
    )
    col2.subheader("All news")
    col2.dataframe(actions_df_all[["Actions", "Num. Seleccion"]].head(len(actions_all)))

    st.markdown("Acciones en noticias verdaderas")
    vars_actions_checked_true = [
        "taf_compartira_familia_amigos",
        "taf_publicara_redes",
        "taf_consultara_fuentes",
        "taf_aplicara_aprendido",
        "taf_no_accion",
    ]
    actions_filt = []
    num_actions_filt = []
    num_actions_str_filt = []
    actions_all = []
    num_actions_all = []
    num_actions_str_all = []
    for var in vars_actions_checked_true:
        actions_filt.append(" ".join(var.split("_")[1:]))
        div_num = df_filt.loc[df_filt[var] != "-", :].shape[0]
        if div_num == 0:
            div_num = 1
        num_act = round(
            df_filt.loc[df_filt[var] == "checked", :].shape[0] / div_num * 100, 1
        )
        num_actions_filt.append(num_act)
        num_actions_str_filt.append(str(num_act) + "%")

        actions_all.append(" ".join(var.split("_")[1:]))
        div_num = df_all.loc[df_all[var] != "-", :].shape[0]
        if div_num == 0:
            div_num = 1
        num_act = round(
            df_all.loc[df_all[var] == "checked", :].shape[0] / div_num * 100, 1
        )
        num_actions_all.append(num_act)
        num_actions_str_all.append(str(num_act) + "%")
    actions_df_filt = pd.DataFrame.from_dict(
        {
            "Actions": actions_filt,
            "Num. Seleccion": num_actions_str_filt,
            "num_act": num_actions_filt,
        }
    )
    actions_df_filt.sort_values(
        by="num_act", ignore_index=True, inplace=True, ascending=False
    )
    actions_df_all = pd.DataFrame.from_dict(
        {
            "Actions": actions_all,
            "Num. Seleccion": num_actions_str_all,
            "num_act": num_actions_all,
        }
    )
    actions_df_all.sort_values(
        by="num_act", ignore_index=True, inplace=True, ascending=False
    )

    col1, col2 = st.beta_columns(2)
    col1.subheader("Filtered news")
    col1.dataframe(
        actions_df_filt[["Actions", "Num. Seleccion"]].head(len(actions_filt))
    )
    col2.subheader("All news")
    col2.dataframe(actions_df_all[["Actions", "Num. Seleccion"]].head(len(actions_all)))


elif section == "Correlaciones":
    st.header(section)
