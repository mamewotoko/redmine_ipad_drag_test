FROM markadams/chromium-xvfb-py2:latest
#RUN apt-get install python-pip
RUN pip install mechanize
RUN curl "https://pypi.python.org/packages/b3/b2/238e2590826bfdd113244a40d9d3eb26918bd798fc187e2360a8367068db/six-1.10.0.tar.gz#md5=34eed507548117b2ab523ab14b2f8b55" > six-1.10.0.tar.gz
RUN tar xfz six-1.10.0.tar.gz
RUN cd six-1.10.0 ; python setup.py install
RUN rm -rf six-*
COPY urllib.py /usr/lib/python2.7/
COPY _form_controls.py /usr/local/lib/python2.7/dist-packages/mechanize/

RUN mkdir -p /opt/work
WORKDIR "/opt/work"
VOLUME ["/opt/work"]
