// static/script.js

document.addEventListener('DOMContentLoaded', function () {
    // Formulário de Registro
    const formRegistro = document.getElementById('form-registro');
    formRegistro.addEventListener('submit', function (event) {
        event.preventDefault();
        const nome = document.getElementById('nome').value;
        const email = document.getElementById('email').value;
        const senha = document.getElementById('senha').value;

        fetch('/registrar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ nome, email, senha })
        })
            .then(response => response.json().then(data => ({ status: response.status, body: data })))
            .then(result => {
                if (result.status === 201) {
                    document.getElementById('mensagem-registro').textContent = 'Registro bem-sucedido!';
                } else {
                    document.getElementById('mensagem-registro').textContent = result.body.msg || 'Erro no registro';
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                document.getElementById('mensagem-registro').textContent = 'Erro ao registrar';
            });
    });

    // Formulário de Login
    const formLogin = document.getElementById('form-login');
    formLogin.addEventListener('submit', function (event) {
        event.preventDefault();
        const email = document.getElementById('email-login').value;
        const senha = document.getElementById('senha-login').value;

        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, senha })
        })
            .then(response => response.json().then(data => ({ status: response.status, body: data })))
            .then(result => {
                if (result.status === 200) {
                    // Armazenar o token JWT
                    localStorage.setItem('jwt', result.body.jwt);
                    document.getElementById('mensagem-login').textContent = 'Login bem-sucedido!';
                    // Exibir a seção de consulta
                    document.getElementById('consulta').style.display = 'block';
                    // Ocultar as seções de registro e login
                    document.getElementById('registro').style.display = 'none';
                    document.getElementById('login').style.display = 'none';
                } else {
                    document.getElementById('mensagem-login').textContent = result.body.msg || 'Erro no login';
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                document.getElementById('mensagem-login').textContent = 'Erro ao fazer login';
            });
    });

    // Formulário de Consulta
    const formConsulta = document.getElementById('form-consulta');
    formConsulta.addEventListener('submit', function (event) {
        event.preventDefault();
        const latitude = document.getElementById('latitude').value;
        const longitude = document.getElementById('longitude').value;
        const jwt = localStorage.getItem('jwt');

        fetch(`/consultar?latitude=${latitude}&longitude=${longitude}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${jwt}`,
                'Accept': 'application/json'
            }
        })
            .then(response => response.json().then(data => ({ status: response.status, body: data })))
            .then(result => {
                if (result.status === 200) {
                    // Exibir os resultados
                    const dados = result.body;
                    let resultadoHTML = '<h3>Dados de Temperatura:</h3><ul>';
                    dados.forEach(item => {
                        // Formatar a data e hora
                        const dataHora = new Date(item.date);
                        const dia = dataHora.getDate().toString().padStart(2, '0');
                        const mes = (dataHora.getMonth() + 1).toString().padStart(2, '0'); // Os meses são indexados a partir de 0
                        const ano = dataHora.getFullYear();
                        const horas = dataHora.getHours().toString().padStart(2, '0');
                        const minutos = dataHora.getMinutes().toString().padStart(2, '0');

                        resultadoHTML += `<li>No dia ${dia}/${mes}/${ano} às ${horas}:${minutos}, a temperatura será de ${item.temperature_2m}°C</li>`;
                    });
                    resultadoHTML += '</ul>';
                    document.getElementById('resultado-consulta').innerHTML = resultadoHTML;
                } else {
                    document.getElementById('resultado-consulta').textContent = result.body.msg || 'Erro na consulta';
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                document.getElementById('resultado-consulta').textContent = 'Erro ao consultar temperatura';
            });
    });
});
