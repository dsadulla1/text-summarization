FROM continuumio/miniconda

COPY app.py /

WORKDIR /

RUN conda update -n base -c defaults conda && \
	conda install python=3.6 git && \
    pip install streamlit bert-extractive-summarizer && \
	conda install pytorch torchvision cudatoolkit=10.0 -c pytorch

EXPOSE 8501

RUN mkdir -p /root/.streamlit

RUN bash -c 'echo -e "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > /root/.streamlit/credentials.toml'

CMD streamlit run app.py --server.port 8501


# New docker image code

# base image
FROM python:3.7

# streamlit-specific commands
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'
RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
" > /root/.streamlit/config.toml'

# exposing default port for streamlit
EXPOSE 8501

# copy over and install packages
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

# copying everything over
COPY . .

# run app
CMD streamlit run webapp/app.py