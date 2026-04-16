const API_URL = (() => {
    const params = new URLSearchParams(window.location.search);
    const apiParam = params.get("api");

    if (apiParam) {
        return apiParam.replace(/\/$/, "");
    }

    const { protocol, hostname, port } = window.location;
    const isLocalFile = protocol === "file:";
    const isHttpServer = port === "5500";

    if (isLocalFile) {
        return "http://127.0.0.1:8000";
    }

    if (isHttpServer) {
        const apiHost = hostname === "localhost" ? "127.0.0.1" : hostname;
        return `${protocol}//${apiHost}:8000`;
    }

    return window.location.origin.replace(/\/$/, "");
})();

function obterUsuarioAtual() {
    return {
        usuario_id: sessionStorage.getItem("usuario_id"),
        tipo: sessionStorage.getItem("tipo"),
    };
}

function paginaInicialPorTipo(tipo) {
    return tipo === "admin" || tipo === "monitor" ? "admin.html" : "botao.html";
}

function protegerPagina(...tiposPermitidos) {
    const { usuario_id, tipo } = obterUsuarioAtual();

    if (!usuario_id || !tipo) {
        window.location.href = "login.html";
        return false;
    }

    if (tiposPermitidos.length && !tiposPermitidos.includes(tipo)) {
        window.location.href = paginaInicialPorTipo(tipo);
        return false;
    }

    return true;
}

async function login() {
    const email = document.getElementById("email")?.value?.trim();
    const senha = document.getElementById("senha")?.value ?? "";

    if (!email || !senha) {
        alert("Preencha email e senha.");
        return;
    }

    try {
        const res = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, senha }),
        });

        const data = await res.json();
        if (!res.ok) {
            throw new Error(data.detail || "Login invalido.");
        }

        sessionStorage.setItem("usuario_id", data.usuario_id);
        sessionStorage.setItem("tipo", data.tipo);
        window.location.href = paginaInicialPorTipo(data.tipo);
    } catch (error) {
        alert(error.message || "Nao foi possivel fazer login.");
    }
}

async function cadastrar() {
    const payload = {
        nome: document.getElementById("nome")?.value?.trim(),
        email: document.getElementById("email")?.value?.trim(),
        cpf: document.getElementById("cpf")?.value?.trim(),
        telefone: document.getElementById("telefone")?.value?.trim(),
        senha: document.getElementById("senha")?.value ?? "",
    };

    if (!payload.nome || !payload.email || !payload.cpf || !payload.telefone || !payload.senha) {
        alert("Preencha todos os campos.");
        return;
    }

    try {
        const res = await fetch(`${API_URL}/usuarios`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        const data = await res.json();
        if (!res.ok) {
            throw new Error(data.detail || "Nao foi possivel cadastrar.");
        }

        alert("Conta criada com sucesso.");
        window.location.href = "login.html";
    } catch (error) {
        alert(error.message || "Nao foi possivel cadastrar.");
    }
}

async function enviarEmergencia() {
    const { usuario_id } = obterUsuarioAtual();
    const statusEl = document.getElementById("status");

    const setStatus = (mensagem, erro = false) => {
        if (!statusEl) {
            return;
        }
        statusEl.textContent = mensagem;
        statusEl.style.color = erro ? "#ffb3b3" : "#8df0b5";
    };

    if (!usuario_id) {
        setStatus("Faca login primeiro.", true);
        window.location.href = "login.html";
        return;
    }

    if (!navigator.geolocation) {
        setStatus("Este navegador nao suporta geolocalizacao.", true);
        return;
    }

    const contextoSeguro =
        window.isSecureContext ||
        window.location.protocol === "https:" ||
        window.location.hostname === "localhost" ||
        window.location.hostname === "127.0.0.1";

    if (!contextoSeguro) {
        setStatus("A localizacao no navegador exige HTTPS ou localhost.", true);
        return;
    }

    setStatus("Solicitando localizacao...");

    navigator.geolocation.getCurrentPosition(
        async (pos) => {
            try {
                const res = await fetch(`${API_URL}/emergencia`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        usuario_id: Number(usuario_id),
                        latitude: pos.coords.latitude,
                        longitude: pos.coords.longitude,
                    }),
                });

                const data = await res.json();
                if (!res.ok) {
                    throw new Error(data.detail || "Erro ao enviar emergencia.");
                }

                setStatus("Emergencia enviada com sucesso.");
            } catch (error) {
                setStatus(error.message || "Erro ao enviar emergencia.", true);
            }
        },
        (error) => {
            const mensagens = {
                1: "Permissao de localizacao negada.",
                2: "Nao foi possivel determinar sua localizacao.",
                3: "A solicitacao de localizacao expirou.",
            };

            setStatus(mensagens[error.code] || "Falha ao obter localizacao.", true);
        },
        {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0,
        }
    );
}

function logout() {
    sessionStorage.clear();
    window.location.href = "login.html";
}

async function carregarEmergencias() {
    const res = await fetch(`${API_URL}/emergencias`);
    const dados = await res.json();

    if (!res.ok) {
        throw new Error(dados.detail || "Erro ao buscar emergencias.");
    }

    return dados;
}
