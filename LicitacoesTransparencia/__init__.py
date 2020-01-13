class Licitacoes:
    # http://www.portaltransparencia.gov.br/licitacoes/consulta?ordenarPor=dataResultadoCompra&direcao=desc
    from datetime import date, datetime

    __status = -1

    __query_params = {
        "paginacaoSimples": "true",
        "tamanhoPagina": 15,
        "offset": 0,
        "direcaoOrdenacao": "desc",
        "colunaOrdenacao": "dataResultadoCompra",
        "de": "01/01/2019",
        "ate": "06/12/2019",
        "colunasSelecionadas": "detalhar,dataResultadoCompra,dataAbertura,orgaoSuperior,orgaoEntidadeVinculada,unidadeGestora,situacao,modalidade,instrumentoLegal,numeroLicitacao,objeto"
    }

    @property
    def url(self):
        from urllib.parse import urlencode
        return f"http://www.portaltransparencia.gov.br/licitacoes/consulta/resultado?{urlencode(self.__query_params)}"

    def request(self) -> map:
        from time import time
        from requests import get
        from LicitacoesTransparencia.objects.licitacao import Licitacao
        self.__query_params["_"] = int(time())

        with get(self.url) as response:
            self.__status = response.status_code
            data = response.json()

        return map(lambda data_obj: Licitacao(data_obj), data)

    @property
    def colunas_selecionadas(self) -> list:
        return self.__query_params["colunasSelecionadas"].split(",")

    @property
    def colunas_selecionadas(self, colunas_selecionadas: list):
        self.__query_params["colunasSelecionadas"] = ",".join(colunas_selecionadas)

    @property
    def desde(self) -> date:
        return self.datetime.strptime(self.__query_params["de"], "%d/%m/%Y").date()

    @desde.setter
    def desde(self, desde: date):
        self.__query_params["de"] = desde.strftime("%d/%m/%Y")

    @property
    def ate(self) -> date:
        return self.datetime.strptime(self.__query_params["ate"], "%d/%m/%Y").date()

    @ate.setter
    def ate(self, ate: date):
        self.__query_params["ate"] = ate.strftime("%d/%m/%Y")

    @property
    def coluna_ordenacao(self) -> str:
        return self.__query_params["colunaOrdenacao"]

    @coluna_ordenacao.setter
    def coluna_ordenacao(self, coluna_ordenacao: str):
        self.__query_params["colunaOrdenacao"] = coluna_ordenacao

    @property
    def direcao_ordenacao(self) -> str:
        return self.__query_params["direcaoOrdenacao"]

    @direcao_ordenacao.setter
    def direcao_ordenacao(self, direcao_ordenacao: str):
        self.__query_params["direcaoOrdenacao"] = direcao_ordenacao

    @property
    def offset(self) -> int:
        return self.__query_params["offset"]

    @offset.setter
    def offset(self, offset: int):
        self.__query_params["offset"] = offset

    @property
    def paginacao_simples(self) -> bool:
        return self.__query_params.get("paginacaoSimples", "false") == "true"

    @paginacao_simples.setter
    def paginacao_simples(self, paginacao_simples: bool):
        self.__query_params["paginacaoSimples"] = "true" if paginacao_simples else "false"

    @property
    def tamanho_pagina(self) -> int:
        return self.__query_params["tamanhoPagina"]

    @tamanho_pagina.setter
    def tamanho_pagina(self, tamanho_pagina: int):
        self.__query_params["tamanhoPagina"] = tamanho_pagina

    def next_page(self):
        self.offset = self.offset + self.tamanho_pagina
        self.request()
        return self.__status

    def prev_page(self):
        self.offset = self.offset - self.tamanho_pagina
        self.request()
        return self.__status
