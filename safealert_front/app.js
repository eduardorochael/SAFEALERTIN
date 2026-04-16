const { useEffect, useState } = React;

const API_URL = window.location.origin;

function App() {
    const [tab, setTab] = useState("login");
    const [session, setSession] = useState(() => ({
        usuarioId: sessionStorage.getItem("usuario_id"),
        tipo: sessionStorage.getItem("tipo"),
    }));
    const [loginForm, setLoginForm] = useState({ email: "", senha: "" });
    const [cadastroForm, setCadastroForm] = useState({
        nome: "",
        email: "",
        cpf: "",
        telefone: "",
        senha: "",
    });
    const [status, setStatus] = useState("");
    const [emergencias, setEmergencias] = useState([]);

    async function api(path, options = {}) {
        const response = await fetch(`${API_URL}${path}`, {
            headers: { "Content-Type": "application/json" },
            ...options,
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || "Erro na requisicao.");
        }
        return data;
    }

    async function handleLogin(event) {
        event.preventDefault();
        try {
            const data = await api("/login", {
                method: "POST",
                body: JSON.stringify(loginForm),
            });

            sessionStorage.setItem("usuario_id", data.usuario_id);
            sessionStorage.setItem("tipo", data.tipo);
            setSession({ usuarioId: String(data.usuario_id), tipo: data.tipo });
            setStatus("Login realizado com sucesso.");
            setTab(data.tipo === "usuario" ? "emergencia" : "painel");
        } catch (error) {
            setStatus(error.message);
        }
    }

    async function handleCadastro(event) {
        event.preventDefault();
        try {
            await api("/usuarios", {
                method: "POST",
                body: JSON.stringify(cadastroForm),
            });
            setStatus("Conta criada com sucesso. Agora faca login.");
            setTab("login");
        } catch (error) {
            setStatus(error.message);
        }
    }

    function logout() {
        sessionStorage.clear();
        setSession({ usuarioId: null, tipo: null });
        setStatus("Sessao encerrada.");
        setTab("login");
    }

    async function enviarEmergencia() {
        if (!session.usuarioId) {
            setStatus("Faca login antes de enviar uma emergencia.");
            return;
        }

        if (!navigator.geolocation) {
            setStatus("Geolocalizacao nao suportada neste navegador.");
            return;
        }

        navigator.geolocation.getCurrentPosition(
            async (position) => {
                try {
                    await api("/emergencia", {
                        method: "POST",
                        body: JSON.stringify({
                            usuario_id: Number(session.usuarioId),
                            latitude: position.coords.latitude,
                            longitude: position.coords.longitude,
                        }),
                    });
                    setStatus("Emergencia enviada com sucesso.");
                    if (session.tipo !== "usuario") {
                        carregarEmergencias();
                    }
                } catch (error) {
                    setStatus(error.message);
                }
            },
            () => setStatus("Nao foi possivel obter a localizacao.")
        );
    }

    async function carregarEmergencias() {
        try {
            const data = await api("/emergencias");
            setEmergencias(data);
        } catch (error) {
            setStatus(error.message);
        }
    }

    useEffect(() => {
        if (session.tipo === "admin" || session.tipo === "monitor") {
            setTab("painel");
            carregarEmergencias();
        } else if (session.tipo === "usuario") {
            setTab("emergencia");
        }
    }, []);

    return (
        <main className="page">
            <section className="card">
                <header className="hero">
                    <div>
                        <p className="eyebrow">Primeiro teste</p>
                        <h1>SafeAlert com FastAPI + React</h1>
                        <p className="subtitle">
                            Frontend React simples servido pelo FastAPI para validar a nova arquitetura.
                        </p>
                    </div>
                    {session.usuarioId ? (
                        <button className="ghost" onClick={logout}>Sair</button>
                    ) : null}
                </header>

                <nav className="tabs">
                    <button className={tab === "login" ? "active" : ""} onClick={() => setTab("login")}>Login</button>
                    <button className={tab === "cadastro" ? "active" : ""} onClick={() => setTab("cadastro")}>Cadastro</button>
                    <button className={tab === "emergencia" ? "active" : ""} onClick={() => setTab("emergencia")}>Emergencia</button>
                    <button className={tab === "painel" ? "active" : ""} onClick={() => { setTab("painel"); carregarEmergencias(); }}>Painel</button>
                </nav>

                {status ? <div className="status">{status}</div> : null}

                {tab === "login" ? (
                    <form className="form" onSubmit={handleLogin}>
                        <input
                            placeholder="Email"
                            type="email"
                            value={loginForm.email}
                            onChange={(e) => setLoginForm({ ...loginForm, email: e.target.value })}
                        />
                        <input
                            placeholder="Senha"
                            type="password"
                            value={loginForm.senha}
                            onChange={(e) => setLoginForm({ ...loginForm, senha: e.target.value })}
                        />
                        <button type="submit">Entrar</button>
                    </form>
                ) : null}

                {tab === "cadastro" ? (
                    <form className="form" onSubmit={handleCadastro}>
                        <input placeholder="Nome" value={cadastroForm.nome} onChange={(e) => setCadastroForm({ ...cadastroForm, nome: e.target.value })} />
                        <input placeholder="Email" type="email" value={cadastroForm.email} onChange={(e) => setCadastroForm({ ...cadastroForm, email: e.target.value })} />
                        <input placeholder="CPF" value={cadastroForm.cpf} onChange={(e) => setCadastroForm({ ...cadastroForm, cpf: e.target.value })} />
                        <input placeholder="Telefone" value={cadastroForm.telefone} onChange={(e) => setCadastroForm({ ...cadastroForm, telefone: e.target.value })} />
                        <input placeholder="Senha" type="password" value={cadastroForm.senha} onChange={(e) => setCadastroForm({ ...cadastroForm, senha: e.target.value })} />
                        <button type="submit">Criar conta</button>
                    </form>
                ) : null}

                {tab === "emergencia" ? (
                    <section className="panel">
                        <p>Use este teste para validar login e envio de localizacao.</p>
                        <button className="danger" onClick={enviarEmergencia}>Enviar emergencia</button>
                    </section>
                ) : null}

                {tab === "painel" ? (
                    <section className="panel">
                        <div className="panel-header">
                            <p>Emergencias registradas</p>
                            <button onClick={carregarEmergencias}>Atualizar</button>
                        </div>
                        <div className="list">
                            {emergencias.length ? emergencias.map((item) => (
                                <article className="list-item" key={item.id}>
                                    <strong>ID {item.id}</strong>
                                    <span>Usuario: {item.usuario?.nome || item.usuario_id}</span>
                                    <span>CPF: {item.usuario?.cpf || "Nao informado"}</span>
                                    <span>Telefone: {item.usuario?.telefone || "Nao informado"}</span>
                                    <span>Latitude: {item.latitude}</span>
                                    <span>Longitude: {item.longitude}</span>
                                    <span>Status: {item.status}</span>
                                </article>
                            )) : <p>Nenhuma emergencia encontrada.</p>}
                        </div>
                    </section>
                ) : null}
            </section>
        </main>
    );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
