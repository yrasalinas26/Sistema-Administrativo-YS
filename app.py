import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página en Streamlit
st.set_page_config(
    page_title="Sistema de Gestión de Condominio",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Código HTML completo de tu aplicación
html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Gestión de Condominio</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <!-- Chart.js para gráficos de morosidad e ingresos -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: #f1f1f1; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
        @media print {
            .no-print { display: none !important; }
            .print-only { display: block !important; }
        }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen flex flex-col">

    <div id="app" class="flex-1 flex flex-col min-h-screen">
        <!-- Toast Notifications Container -->
        <div id="toast-container" class="fixed top-4 right-4 z-50 flex flex-col gap-2 pointer-events-none"></div>

        <!-- APP CONTENT WILL BE DYNAMICALLY INJECTED HERE -->
    </div>

    <script>
        // --- DATA INITIALIZATION & LOCAL STORAGE ---
        const DEFAULT_BUILDING_INFO = {
            name: "Residencias El Roble",
            rif: "J-30982341-0",
            address: "Calle Los Almendros, Av. Principal, Urb. Altamira, Caracas",
            logoUrl: "https://placehold.co/150x150/2563eb/ffffff?text=CONDOMINIO",
            bcvRate: 36.50,
            lastBcvUpdate: new Date().toISOString().split('T')[0]
        };

        const APARTMENTS_DATA = [
            { id: "1A", owner: "Carlos Mendoza", phone: "+584141234567", email: "carlos@gmail.com", alicuota: 6 },
            { id: "1B", owner: "María Rodríguez", phone: "+584242345678", email: "maria@gmail.com", alicuota: 6 },
            { id: "2",  owner: "Inversiones R&S C.A.", phone: "+584123456789", email: "contacto@inversiones.com", alicuota: 12 },
            { id: "3A", owner: "José Luis Gómez", phone: "+584164567890", email: "jose.gomez@hotmail.com", alicuota: 6 },
            { id: "3B", owner: "Ana Belén Torres", phone: "+584145678901", email: "atorres@yahoo.com", alicuota: 6 },
            { id: "4A", owner: "Roberto Hernández", phone: "+584246789012", email: "roberto.h@gmail.com", alicuota: 6 },
            { id: "4B", owner: "Elena Castillo", phone: "+584127890123", email: "ecastillo@outlook.com", alicuota: 6 },
            { id: "5A", owner: "Fernando Morales", phone: "+584148901234", email: "fmorales@gmail.com", alicuota: 6 },
            { id: "5B", owner: "Patricia Silva", phone: "+584249012345", email: "p.silva@gmail.com", alicuota: 6 },
            { id: "6A", owner: "Gabriel Vargas", phone: "+584120123456", email: "gvargas@gmail.com", alicuota: 6 },
            { id: "6B", owner: "Sofia Ramírez", phone: "+584141122334", email: "sramirez@gmail.com", alicuota: 6 },
            { id: "7",  owner: "Servicios Corporativos T&T", phone: "+584242233445", email: "servicios@tyt.com", alicuota: 12 },
            { id: "PH", owner: "Alejandro Blanco", phone: "+584123344556", email: "ablanco@ph.com", alicuota: 16 }
        ];

        const INITIAL_EXPENSES = [
            { id: "EXP-01", period: "2026-02", description: "Servicio de Vigilancia 24/7", category: "Servicios", amountUSD: 450.00, isUncommon: false, targetApt: "ALL", date: "2026-02-05", supplier: "Seguridad Integral C.A." },
            { id: "EXP-02", period: "2026-02", description: "Mantenimiento Preventivo de Ascensores", category: "Mantenimiento", amountUSD: 280.00, isUncommon: false, targetApt: "ALL", date: "2026-02-10", supplier: "Ascensores Rápido S.A." },
            { id: "EXP-03", period: "2026-02", description: "Electricidad Áreas Comunes (CORPOELEC)", category: "Servicios", amountUSD: 120.00, isUncommon: false, targetApt: "ALL", date: "2026-02-15", supplier: "CORPOELEC" },
            { id: "EXP-04", period: "2026-02", description: "Reparación fuga de agua interna apto 4A", category: "Reparaciones Especiales", amountUSD: 65.00, isUncommon: true, targetApt: "4A", date: "2026-02-18", supplier: "Plomería Express" }
        ];

        const INITIAL_EXTRA_QUOTAS = [
            { id: "EQ-01", period: "2026-02", title: "Fondo de Reserva para Pintura Fachada", description: "Cuota 1/3 para restauración de paredes exteriores", totalAmountUSD: 600.00, date: "2026-02-01" }
        ];

        const INITIAL_SUPPLIERS = [
            { id: "SUP-01", name: "Seguridad Integral C.A.", rif: "J-40112233-4", service: "Vigilancia", phone: "0414-1112233", email: "contacto@seguridad.com" },
            { id: "SUP-02", name: "Ascensores Rápido S.A.", rif: "J-30223344-5", service: "Mantenimiento Ascensores", phone: "0412-2223344", email: "soporte@ascensores.com" },
            { id: "SUP-03", name: "Plomería Express", rif: "J-50334455-6", service: "Reparaciones e Hidráulica", phone: "0424-3334455", email: "plomeriaexpress@gmail.com" },
            { id: "SUP-04", name: "CORPOELEC", rif: "J-00000000-0", service: "Electricidad", phone: "0800-5555555", email: "pagos@corpoelec.gob.ve" }
        ];

        const INITIAL_PAYMENTS = [
            { id: "PAY-101", aptId: "1A", period: "2026-01", amountUSD: 85.00, amountBs: 3060.00, rateBCV: 36.00, currency: "BS", method: "Pago Móvil", reference: "998821", date: "2026-01-28", status: "APPROVED", note: "Cobro Enero" },
            { id: "PAY-102", aptId: "2", period: "2026-01", amountUSD: 170.00, amountBs: 6120.00, rateBCV: 36.00, currency: "USD", method: "Efectivo USD", reference: "REC-0012", date: "2026-01-29", status: "APPROVED", note: "Cobro Enero" },
            { id: "PAY-103", aptId: "PH", period: "2026-02", amountUSD: 241.60, amountBs: 8818.40, rateBCV: 36.50, currency: "BS", method: "Transferencia", reference: "12345678", date: "2026-02-20", status: "PENDING", note: "Pago aviso Febrero" },
            { id: "PAY-104", aptId: "3A", period: "2026-02", amountUSD: 90.60, amountBs: 3306.90, rateBCV: 36.50, currency: "BS", method: "Pago Móvil", reference: "55443322", date: "2026-02-22", status: "PENDING", note: "Aviso Feb" }
        ];

        class StateManager {
            constructor() {
                this.loadState();
            }
            loadState() {
                this.building = JSON.parse(localStorage.getItem('condo_building')) || DEFAULT_BUILDING_INFO;
                this.apartments = JSON.parse(localStorage.getItem('condo_apartments')) || APARTMENTS_DATA;
                this.expenses = JSON.parse(localStorage.getItem('condo_expenses')) || INITIAL_EXPENSES;
                this.extraQuotas = JSON.parse(localStorage.getItem('condo_extra_quotas')) || INITIAL_EXTRA_QUOTAS;
                this.suppliers = JSON.parse(localStorage.getItem('condo_suppliers')) || INITIAL_SUPPLIERS;
                this.payments = JSON.parse(localStorage.getItem('condo_payments')) || INITIAL_PAYMENTS;
                
                const defaultPasswords = {};
                this.apartments.forEach(a => defaultPasswords[a.id] = "123456");
                defaultPasswords['admin'] = "admin123";
                this.passwords = JSON.parse(localStorage.getItem('condo_passwords')) || defaultPasswords;

                this.currentUser = JSON.parse(sessionStorage.getItem('condo_user')) || null;
                this.selectedPeriod = "2026-02";
            }
            saveState() {
                localStorage.setItem('condo_building', JSON.stringify(this.building));
                localStorage.setItem('condo_apartments', JSON.stringify(this.apartments));
                localStorage.setItem('condo_expenses', JSON.stringify(this.expenses));
                localStorage.setItem('condo_extra_quotas', JSON.stringify(this.extraQuotas));
                localStorage.setItem('condo_suppliers', JSON.stringify(this.suppliers));
                localStorage.setItem('condo_payments', JSON.stringify(this.payments));
                localStorage.setItem('condo_passwords', JSON.stringify(this.passwords));
            }
            login(role, aptId, password) {
                if (role === 'admin') {
                    if (password === this.passwords['admin']) {
                        this.currentUser = { role: 'admin', name: 'Administrador / Junta' };
                        sessionStorage.setItem('condo_user', JSON.stringify(this.currentUser));
                        return true;
                    }
                } else if (role === 'owner') {
                    if (this.passwords[aptId] && password === this.passwords[aptId]) {
                        const apt = this.apartments.find(a => a.id === aptId);
                        this.currentUser = { role: 'owner', aptId: aptId, name: apt ? apt.owner : `Propietario ${aptId}` };
                        sessionStorage.setItem('condo_user', JSON.stringify(this.currentUser));
                        return true;
                    }
                }
                return false;
            }
            logout() {
                this.currentUser = null;
                sessionStorage.removeItem('condo_user');
                renderApp();
            }
        }

        const appState = new StateManager();

        function formatUSD(amount) {
            return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount || 0);
        }
        function formatBS(amount) {
            return new Intl.NumberFormat('es-VE', { style: 'currency', currency: 'VES' }).format(amount || 0).replace('VES', 'Bs.');
        }
        function showToast(message, type = 'success') {
            const container = document.getElementById('toast-container');
            if (!container) return;
            const toast = document.createElement('div');
            const bgClass = type === 'success' ? 'bg-emerald-600' : type === 'error' ? 'bg-rose-600' : 'bg-blue-600';
            toast.className = `pointer-events-auto flex items-center gap-2 text-white px-4 py-3 rounded-lg shadow-lg text-sm transition-all duration-300 transform translate-y-2 opacity-0 ${bgClass}`;
            toast.innerHTML = `<span>${message}</span>`;
            container.appendChild(toast);
            setTimeout(() => toast.classList.remove('translate-y-2', 'opacity-0'), 10);
            setTimeout(() => {
                toast.classList.add('opacity-0', 'translate-y-2');
                setTimeout(() => toast.remove(), 300);
            }, 3500);
        }

        function renderApp() {
            const app = document.getElementById('app');
            if (!appState.currentUser) {
                app.innerHTML = renderLoginScreen();
            } else {
                app.innerHTML = `<div class="p-6"><h1 class="text-xl font-bold">Panel Principal</h1><p>Sesión activa como: ${appState.currentUser.name}</p><button onclick="appState.logout()" class="mt-4 px-4 py-2 bg-red-600 text-white rounded">Cerrar Sesión</button></div>`;
            }
            if (typeof lucide !== 'undefined') lucide.createIcons();
        }

        function renderLoginScreen() {
            return `
            <div class="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-950 flex items-center justify-center p-4">
                <div class="max-w-md w-full bg-white rounded-2xl shadow-2xl overflow-hidden border border-slate-100 p-6 text-center">
                    <h1 class="text-2xl font-bold text-slate-800 mb-2">${appState.building.name}</h1>
                    <p class="text-xs text-slate-500 mb-6">RIF: ${appState.building.rif}</p>
                    <button onclick="quickLogin('admin')" class="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm rounded-lg shadow-md mb-3">
                        Entrar como Administrador
                    </button>
                </div>
            </div>`;
        }

        function quickLogin(role) {
            appState.login('admin', null, 'admin123');
            showToast("¡Bienvenido al sistema!");
            renderApp();
        }

        // Inicializar aplicación al cargar
        window.onload = function() {
            renderApp();
        };
    </script>
</body>
</html>
"""

# Renderizar el HTML en Streamlit con altura adaptable
components.html(html_code, height=850, scrolling=True)
