// 🔥 Inicializa mapa
let map =

L.tileLayer();

let markers = [];

// 🚀 Buscar endereço (lat/lon → endereço)
async function buscarEndereco(lat, lon) {
    try {
        const res = await fetch(
            `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`
        );
        const data = await res.json();
        return data.display_name || "Endereço não encontrado";
    } catch {
        return "Erro ao buscar endereço";
    }
}

// 🔥 Carregar emergências + mapa + usuário
async function carregarLista() {
    const status = document.getElementById("status");
    const lista = document.getElementById("lista-emergencias");

    try {
        const alertas = await carregarEmergencias();

        // limpa lista
        lista.innerHTML = "";

        // limpa mapa
        markers.forEach(m => map.removeLayer(m));
        markers = [];

        if (!alertas.length) {
            status.textContent = "Nenhuma emergencia registrada.";
            return;
        }

        status.textContent = `${alertas.length} emergencia(s) encontrada(s).`;

        let bounds = [];

        for (const alerta of alertas) {

            // 🔥 pega dados do usuário
            const nome = alerta.usuario?.nome || "Não informado";
            const telefone = alerta.usuario?.telefone || "Não informado";

            // 🔥 busca endereço
            const endereco = await buscarEndereco(alerta.latitude, alerta.longitude);

            // 📋 lista na tela
            lista.innerHTML += `
                <div class="card-alerta">
                    <strong>ID ${alerta.id}</strong><br>
                    👤 Nome: ${nome}<br>
                    📞 Telefone: ${telefone}<br>
                    📍 ${endereco}<br>
                    Status: ${alerta.status}
                </div>
            `;

            // 📍 marcador no mapa
            const marker = L.marker([alerta.latitude, alerta.longitude])
                .addTo(map)
                .bindPopup(`
                    <b>🚨 Emergência ID ${alerta.id}</b><br>
                    👤 ${nome}<br>
                    📞 ${telefone}<br>
                    📍 ${endereco}<br>
                    Status: ${alerta.status}
                `);

            markers.push(marker);
            bounds.push([alerta.latitude, alerta.longitude]);
        }

        // 🎯 centraliza mapa
        if (bounds.length > 0) {
            map.fitBounds(bounds);
        }

    } catch (error) {
        status.textContent = error.message || "Erro ao carregar emergencias.";
    }
}

// 🔐 Proteção + auto atualização
if (protegerPagina("admin", "monitor")) {
    carregarLista();
    setInterval(carregarLista, 5000);
}