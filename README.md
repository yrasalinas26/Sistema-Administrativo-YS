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

        // Seed Expenses
        const INITIAL_EXPENSES = [
            { id: "EXP-01", period: "2026-02", description: "Servicio de Vigilancia 24/7", category: "Servicios", amountUSD: 450.00, isUncommon: false, targetApt: "ALL", date: "2026-02-05", supplier: "Seguridad Integral C.A." },
            { id: "EXP-02", period: "2026-02", description: "Mantenimiento Preventivo de Ascensores", category: "Mantenimiento", amountUSD: 280.00, isUncommon: false, targetApt: "ALL", date: "2026-02-10", supplier: "Ascensores Rápido S.A." },
            { id: "EXP-03", period: "2026-02", description: "Electricidad Áreas Comunes (CORPOELEC)", category: "Servicios", amountUSD: 120.00, isUncommon: false, targetApt: "ALL", date: "2026-02-15", supplier: "CORPOELEC" },
            { id: "EXP-04", period: "2026-02", description: "Reparación fuga de agua interna apto 4A", category: "Reparaciones Especiales", amountUSD: 65.00, isUncommon: true, targetApt: "4A", date: "2026-02-18", supplier: "Plomería Express" }
        ];

        // Seed Extra Quotas
        const INITIAL_EXTRA_QUOTAS = [
            { id: "EQ-01", period: "2026-02", title: "Fondo de Reserva para Pintura Fachada", description: "Cuota 1/3 para restauración de paredes exteriores", totalAmountUSD: 600.00, date: "2026-02-01" }
        ];

        // Seed Suppliers
        const INITIAL_SUPPLIERS = [
            { id: "SUP-01", name: "Seguridad Integral C.A.", rif: "J-40112233-4", service: "Vigilancia", phone: "0414-1112233", email: "contacto@seguridad.com" },
            { id: "SUP-02", name: "Ascensores Rápido S.A.", rif: "J-30223344-5", service: "Mantenimiento Ascensores", phone: "0412-2223344", email: "soporte@ascensores.com" },
            { id: "SUP-03", name: "Plomería Express", rif: "J-50334455-6", service: "Reparaciones e Hidráulica", phone: "0424-3334455", email: "plomeriaexpress@gmail.com" },
            { id: "SUP-04", name: "CORPOELEC", rif: "J-00000000-0", service: "Electricidad", phone: "0800-5555555", email: "pagos@corpoelec.gob.ve" }
        ];

        // Seed Payments
        const INITIAL_PAYMENTS = [
            { id: "PAY-101", aptId: "1A", period: "2026-01", amountUSD: 85.00, amountBs: 3060.00, rateBCV: 36.00, currency: "BS", method: "Pago Móvil", reference: "998821", date: "2026-01-28", status: "APPROVED", note: "Cobro Enero" },
            { id: "PAY-102", aptId: "2", period: "2026-01", amountUSD: 170.00, amountBs: 6120.00, rateBCV: 36.00, currency: "USD", method: "Efectivo USD", reference: "REC-0012", date: "2026-01-29", status: "APPROVED", note: "Cobro Enero" },
            { id: "PAY-103", aptId: "PH", period: "2026-02", amountUSD: 241.60, amountBs: 8818.40, rateBCV: 36.50, currency: "BS", method: "Transferencia", reference: "12345678", date: "2026-02-20", status: "PENDING", note: "Pago aviso Febrero" },
            { id: "PAY-104", aptId: "3A", period: "2026-02", amountUSD: 90.60, amountBs: 3306.90, rateBCV: 36.50, currency: "BS", method: "Pago Móvil", reference: "55443322", date: "2026-02-22", status: "PENDING", note: "Aviso Feb" }
        ];

        // Application State Management
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
                
                // User Passwords (aptId -> password)
                const defaultPasswords = {};
                this.apartments.forEach(a => defaultPasswords[a.id] = "123456");
                defaultPasswords['admin'] = "admin123";
                this.passwords = JSON.parse(localStorage.getItem('condo_passwords')) || defaultPasswords;

                // Current Session
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

            resetPassword(userId, newPassword) {
                this.passwords[userId] = newPassword;
                this.saveState();
            }
        }

        const appState = new StateManager();

        // --- HELPER FUNCTIONS ---
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
            toast.innerHTML = `<i data-lucide="${type === 'success' ? 'check-circle' : type === 'error' ? 'alert-triangle' : 'info'}" class="w-5 h-5"></i><span>${message}</span>`;
            container.appendChild(toast);
            lucide.createIcons();
            
            setTimeout(() => {
                toast.classList.remove('translate-y-2', 'opacity-0');
            }, 10);

            setTimeout(() => {
                toast.classList.add('opacity-0', 'translate-y-2');
                setTimeout(() => toast.remove(), 300);
            }, 3500);
        }

        // --- CALCULATIONS FOR BILLING ---
        function calculatePeriodTotalUSD(period) {
            // Common expenses total
            const commonExpensesUSD = appState.expenses
                .filter(e => e.period === period && !e.isUncommon)
                .reduce((sum, e) => sum + Number(e.amountUSD), 0);

            // Extra quotas total
            const extraQuotasUSD = appState.extraQuotas
                .filter(eq => eq.period === period)
                .reduce((sum, eq) => sum + Number(eq.totalAmountUSD), 0);

            return commonExpensesUSD + extraQuotasUSD;
        }

        function calculateAptBill(aptId, period) {
            const apt = appState.apartments.find(a => a.id === aptId);
            if (!apt) return { totalUSD: 0, totalBS: 0, commonUSD: 0, extraUSD: 0, uncommonUSD: 0 };

            // 1. Common Expenses share by Alicuota
            const commonTotalUSD = appState.expenses
                .filter(e => e.period === period && !e.isUncommon)
                .reduce((sum, e) => sum + Number(e.amountUSD), 0);
            const aptCommonUSD = (commonTotalUSD * apt.alicuota) / 100;

            // 2. Extra Quotas share by Alicuota
            const extraTotalUSD = appState.extraQuotas
                .filter(eq => eq.period === period)
                .reduce((sum, eq) => sum + Number(eq.totalAmountUSD), 0);
            const aptExtraUSD = (extraTotalUSD * apt.alicuota) / 100;

            // 3. Uncommon Expenses for specific apartment
            const aptUncommonUSD = appState.expenses
                .filter(e => e.period === period && e.isUncommon && e.targetApt === aptId)
                .reduce((sum, e) => sum + Number(e.amountUSD), 0);

            const totalUSD = aptCommonUSD + aptExtraUSD + aptUncommonUSD;
            const totalBS = totalUSD * appState.building.bcvRate;

            return {
                apt,
                commonTotalUSD,
                aptCommonUSD,
                aptExtraUSD,
                aptUncommonUSD,
                totalUSD,
                totalBS,
                rateBCV: appState.building.bcvRate
            };
        }

        function calculateAptBalance(aptId) {
            // Sum all approved payments
            const approvedPayments = appState.payments
                .filter(p => p.aptId === aptId && p.status === 'APPROVED')
                .reduce((sum, p) => sum + Number(p.amountUSD), 0);

            // Sum all bills up to current period
            // For simplicity in mock data, we evaluate 2026-01 and 2026-02
            const periods = ["2026-01", "2026-02"];
            let totalBilledUSD = 0;
            periods.forEach(p => {
                const bill = calculateAptBill(aptId, p);
                totalBilledUSD += bill.totalUSD;
            });

            const diff = approvedPayments - totalBilledUSD;
            return {
                billedUSD: totalBilledUSD,
                paidUSD: approvedPayments,
                balanceUSD: diff // positive = credit, negative = debt
            };
        }

        // --- RENDER MAIN LAYOUT & NAVIGATION ---
        function renderApp() {
            const app = document.getElementById('app');
            if (!appState.currentUser) {
                app.innerHTML = renderLoginScreen();
            } else if (appState.currentUser.role === 'admin') {
                app.innerHTML = renderAdminLayout();
            } else if (appState.currentUser.role === 'owner') {
                app.innerHTML = renderOwnerLayout();
            }
            lucide.createIcons();
        }

        function renderLoginScreen() {
            return `
            <div class="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-950 flex items-center justify-center p-4">
                <div class="max-w-md w-full bg-white rounded-2xl shadow-2xl overflow-hidden border border-slate-100">
                    <div class="bg-blue-600 p-6 text-center text-white relative">
                        <div class="w-20 h-20 bg-white rounded-full mx-auto flex items-center justify-center shadow-md mb-3 border-4 border-blue-400 overflow-hidden">
                            <img src="${appState.building.logoUrl}" alt="Logo" class="w-full h-full object-cover" onerror="this.src='https://placehold.co/150x150/2563eb/ffffff?text=CONDOMINIO'">
                        </div>
                        <h1 class="text-2xl font-bold tracking-tight">${appState.building.name}</h1>
                        <p class="text-blue-100 text-xs mt-1">RIF: ${appState.building.rif}</p>
                    </div>

                    <div class="p-6">
                        <!-- Quick Role Switcher Tabs -->
                        <div class="flex rounded-lg bg-slate-100 p-1 mb-6">
                            <button onclick="toggleLoginType('admin')" id="tab-admin" class="flex-1 py-2 text-xs font-semibold rounded-md transition-all bg-white text-blue-600 shadow-sm">
                                Administrador / Junta
                            </button>
                            <button onclick="toggleLoginType('owner')" id="tab-owner" class="flex-1 py-2 text-xs font-semibold rounded-md transition-all text-slate-600 hover:text-slate-900">
                                Propietario
                            </button>
                        </div>

                        <!-- Login Form -->
                        <form id="login-form" onsubmit="handleLogin(event)" class="space-y-4">
                            <input type="hidden" id="login-role" value="admin">
                            
                            <div id="apt-selector-container" class="hidden">
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Seleccionar Apartamento</label>
                                <select id="login-apt" class="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                                    ${appState.apartments.map(a => `<option value="${a.id}">Apartamento ${a.id} (${a.owner})</option>`).join('')}
                                </select>
                            </div>

                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Contraseña</label>
                                <input type="password" id="login-password" value="admin123" required placeholder="••••••••" class="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                            </div>

                            <button type="submit" class="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm rounded-lg shadow-md transition-all flex items-center justify-center gap-2">
                                <i data-lucide="log-in" class="w-4 h-4"></i> Iniciar Sesión
                            </button>
                        </form>

                        <!-- Fast Demo Login Buttons -->
                        <div class="mt-8 pt-6 border-t border-slate-100">
                            <p class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3 text-center">Acceso Rápido para Demostración</p>
                            <div class="grid grid-cols-2 gap-2">
                                <button onclick="quickLogin('admin')" class="p-2 border border-blue-200 hover:bg-blue-50 text-blue-700 rounded-lg text-xs font-medium flex items-center justify-center gap-1">
                                    <i data-lucide="shield" class="w-3.5 h-3.5"></i> Entrar como Admin
                                </button>
                                <button onclick="quickLogin('owner', '1A')" class="p-2 border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-lg text-xs font-medium flex items-center justify-center gap-1">
                                    <i data-lucide="home" class="w-3.5 h-3.5"></i> Entrar como Apto 1A
                                </button>
                                <button onclick="quickLogin('owner', '2')" class="p-2 border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-lg text-xs font-medium flex items-center justify-center gap-1">
                                    <i data-lucide="home" class="w-3.5 h-3.5"></i> Entrar como Apto 2
                                </button>
                                <button onclick="quickLogin('owner', 'PH')" class="p-2 border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-lg text-xs font-medium flex items-center justify-center gap-1">
                                    <i data-lucide="crown" class="w-3.5 h-3.5"></i> Entrar como PH
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            `;
        }

        function toggleLoginType(role) {
            document.getElementById('login-role').value = role;
            const tabAdmin = document.getElementById('tab-admin');
            const tabOwner = document.getElementById('tab-owner');
            const aptContainer = document.getElementById('apt-selector-container');
            const pwdInput = document.getElementById('login-password');

            if (role === 'admin') {
                tabAdmin.className = "flex-1 py-2 text-xs font-semibold rounded-md transition-all bg-white text-blue-600 shadow-sm";
                tabOwner.className = "flex-1 py-2 text-xs font-semibold rounded-md transition-all text-slate-600 hover:text-slate-900";
                aptContainer.classList.add('hidden');
                pwdInput.value = "admin123";
            } else {
                tabOwner.className = "flex-1 py-2 text-xs font-semibold rounded-md transition-all bg-white text-blue-600 shadow-sm";
                tabAdmin.className = "flex-1 py-2 text-xs font-semibold rounded-md transition-all text-slate-600 hover:text-slate-900";
                aptContainer.classList.remove('hidden');
                pwdInput.value = "123456";
            }
        }

        function handleLogin(e) {
            e.preventDefault();
            const role = document.getElementById('login-role').value;
            const aptId = document.getElementById('login-apt').value;
            const password = document.getElementById('login-password').value;

            if (appState.login(role, aptId, password)) {
                showToast(`Bienvenido al sistema ${appState.currentUser.name}`);
                renderApp();
            } else {
                showToast("Contraseña incorrecta. Por favor intente de nuevo.", "error");
            }
        }

        function quickLogin(role, aptId = "1A") {
            if (role === 'admin') {
                appState.login('admin', null, 'admin123');
            } else {
                appState.login('owner', aptId, '123456');
            }
            showToast(`Ingresó como ${appState.currentUser.name}`);
            renderApp();
        }

        let currentAdminTab = 'expenses'; // Default tab

        function renderAdminLayout() {
            return `
            <div class="flex-1 flex flex-col md:flex-row bg-slate-100 min-h-screen">
                <!-- Sidebar Header Navigation -->
                <aside class="w-full md:w-64 bg-slate-900 text-slate-200 flex flex-col shrink-0 no-print">
                    <div class="p-4 border-b border-slate-800 flex items-center justify-between">
                        <div class="flex items-center gap-3">
                            <img src="${appState.building.logoUrl}" class="w-10 h-10 rounded-lg object-cover bg-white p-0.5" alt="Logo">
                            <div class="overflow-hidden">
                                <h2 class="text-sm font-bold text-white leading-tight truncate">${appState.building.name}</h2>
                                <p class="text-[10px] text-blue-400 font-mono">${appState.building.rif}</p>
                            </div>
                        </div>
                    </div>

                    <!-- BCV Live Bar -->
                    <div class="px-4 py-3 bg-slate-800/80 border-b border-slate-800 flex items-center justify-between text-xs">
                        <span class="text-slate-400 flex items-center gap-1">
                            <i data-lucide="dollar-sign" class="w-3.5 h-3.5 text-emerald-400"></i> Tasa BCV:
                        </span>
                        <div class="flex items-center gap-1 font-bold text-emerald-400">
                            Bs. ${appState.building.bcvRate.toFixed(2)}
                            <button onclick="openBcvModal()" title="Modificar Tasa BCV" class="hover:bg-slate-700 p-1 rounded text-slate-300">
                                <i data-lucide="edit-2" class="w-3 h-3"></i>
                            </button>
                        </div>
                    </div>

                    <!-- Navigation Links -->
                    <nav class="flex-1 p-3 space-y-1 text-xs overflow-y-auto custom-scrollbar">
                        <p class="px-3 py-1 text-[10px] font-bold text-slate-500 uppercase tracking-wider">Gestión Principal</p>
                        <button onclick="switchAdminTab('expenses')" class="nav-btn ${currentAdminTab === 'expenses' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800'} w-full text-left px-3 py-2.5 rounded-lg font-medium flex items-center gap-2.5 transition">
                            <i data-lucide="receipt" class="w-4 h-4"></i> Distribución de Gastos
                        </button>
                        <button onclick="switchAdminTab('extraQuotas')" class="nav-btn ${currentAdminTab === 'extraQuotas' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800'} w-full text-left px-3 py-2.5 rounded-lg font-medium flex items-center gap-2.5 transition">
                            <i data-lucide="piggy-bank" class="w-4 h-4"></i> Cuotas Extraordinarias
                        </button>
                        <button onclick="switchAdminTab('payments')" class="nav-btn ${currentAdminTab === 'payments' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800'} w-full text-left px-3 py-2.5 rounded-lg font-medium flex items-center justify-between transition">
                            <span class="flex items-center gap-2.5">
                                <i data-lucide="check-square" class="w-4 h-4"></i> Conciliación de Pagos
                            </span>
                            ${countPendingPayments() > 0 ? `<span class="bg-rose-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full">${countPendingPayments()}</span>` : ''}
                        </button>
                        <button onclick="switchAdminTab('whatsapp')" class="nav-btn ${currentAdminTab === 'whatsapp' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800'} w-full text-left px-3 py-2.5 rounded-lg font-medium flex items-center gap-2.5 transition">
                            <i data-lucide="message-square" class="w-4 h-4 text-emerald-400"></i> Avisos WhatsApp
                        </button>
                        <button onclick="switchAdminTab('directPayment')" class="nav-btn ${currentAdminTab === 'directPayment' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800'} w-full text-left px-3 py-2.5 rounded-lg font-medium flex items-center gap-2.5 transition">
                            <i data-lucide="plus-circle" class="w-4 h-4"></i> Registrar Pago Manual
                        </button>

                        <p class="px-3 py-1 mt-4 text-[10px] font-bold text-slate-500 uppercase tracking-wider">Monitoreo & Reportes</p>
                        <button onclick="switchAdminTab('dashboard')" class="nav-btn ${currentAdminTab === 'dashboard' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800'} w-full text-left px-3 py-2.5 rounded-lg font-medium flex items-center gap-2.5 transition">
                            <i data-lucide="bar-chart-3" class="w-4 h-4"></i> Morosidad y Finanzas
                        </button>
                        <button onclick="switchAdminTab('suppliers')" class="nav-btn ${currentAdminTab === 'suppliers' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800'} w-full text-left px-3 py-2.5 rounded-lg font-medium flex items-center gap-2.5 transition">
                            <i data-lucide="truck" class="w-4 h-4"></i> Proveedores
                        </button>
                        <button onclick="switchAdminTab('reports')" class="nav-btn ${currentAdminTab === 'reports' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800'} w-full text-left px-3 py-2.5 rounded-lg font-medium flex items-center gap-2.5 transition">
                            <i data-lucide="file-spreadsheet" class="w-4 h-4"></i> Reportes de Gestión
                        </button>

                        <p class="px-3 py-1 mt-4 text-[10px] font-bold text-slate-500 uppercase tracking-wider">Configuración</p>
                        <button onclick="switchAdminTab('census')" class="nav-btn ${currentAdminTab === 'census' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800'} w-full text-left px-3 py-2.5 rounded-lg font-medium flex items-center gap-2.5 transition">
                            <i data-lucide="users" class="w-4 h-4"></i> Censo & Alícuotas
                        </button>
                        <button onclick="switchAdminTab('settings')" class="nav-btn ${currentAdminTab === 'settings' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800'} w-full text-left px-3 py-2.5 rounded-lg font-medium flex items-center gap-2.5 transition">
                            <i data-lucide="building" class="w-4 h-4"></i> Datos del Condominio
                        </button>
                    </nav>

                    <div class="p-3 border-t border-slate-800 flex items-center justify-between text-xs">
                        <div class="flex items-center gap-2">
                            <div class="w-7 h-7 rounded-full bg-blue-500 flex items-center justify-center font-bold text-white text-xs">A</div>
                            <div>
                                <p class="font-medium text-white truncate w-28">Administrador</p>
                                <p class="text-[10px] text-slate-400">Junta de Condominio</p>
                            </div>
                        </div>
                        <button onclick="appState.logout()" title="Cerrar Sesión" class="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded">
                            <i data-lucide="log-out" class="w-4 h-4"></i>
                        </button>
                    </div>
                </aside>

                <!-- Main Admin Content Body -->
                <main class="flex-1 overflow-y-auto p-4 md:p-6 custom-scrollbar">
                    ${renderAdminTabContent()}
                </main>
            </div>

            <!-- Global BCV Rate Modal -->
            <div id="bcv-modal" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center hidden">
                <div class="bg-white rounded-xl shadow-xl max-w-sm w-full p-6 border border-slate-100">
                    <h3 class="text-base font-bold text-slate-800 mb-2 flex items-center gap-2">
                        <i data-lucide="refresh-cw" class="w-5 h-5 text-blue-600"></i> Actualizar Tasa Oficial BCV
                    </h3>
                    <p class="text-xs text-slate-500 mb-4">Ingrese la tasa oficial en Bolívares para las conversiones automáticas del condominio.</p>
                    
                    <div class="space-y-3">
                        <div>
                            <label class="block text-xs font-medium text-slate-700 mb-1">Tasa (Bs / USD)</label>
                            <input type="number" id="input-bcv-rate" step="0.01" value="${appState.building.bcvRate}" class="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500">
                        </div>
                        <div class="p-2 bg-blue-50 rounded-lg text-[11px] text-blue-700 flex justify-between items-center">
                            <span>Simular tasa BCV en tiempo real</span>
                            <button onclick="simulateBcvFetch()" class="text-xs font-bold underline hover:text-blue-900">Auto-obtener</button>
                        </div>
                    </div>

                    <div class="flex justify-end gap-2 mt-6">
                        <button onclick="closeBcvModal()" class="px-3 py-1.5 text-xs text-slate-600 hover:bg-slate-100 rounded-lg">Cancelar</button>
                        <button onclick="saveBcvRate()" class="px-4 py-1.5 text-xs bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg">Guardar Tasa</button>
                    </div>
                </div>
            </div>
            `;
        }

        function switchAdminTab(tab) {
            currentAdminTab = tab;
            renderApp();
        }

        function countPendingPayments() {
            return appState.payments.filter(p => p.status === 'PENDING').length;
        }

        function openBcvModal() {
            document.getElementById('bcv-modal').classList.remove('hidden');
        }

        function closeBcvModal() {
            document.getElementById('bcv-modal').classList.add('hidden');
        }

        function saveBcvRate() {
            const val = parseFloat(document.getElementById('input-bcv-rate').value);
            if (!isNaN(val) && val > 0) {
                appState.building.bcvRate = val;
                appState.building.lastBcvUpdate = new Date().toISOString().split('T')[0];
                appState.saveState();
                closeBcvModal();
                showToast(`Tasa BCV actualizada a Bs. ${val.toFixed(2)}`);
                renderApp();
            }
        }

        function simulateBcvFetch() {
            // Random small fluctuation for realistic simulation
            const current = appState.building.bcvRate;
            const simulated = +(current + (Math.random() * 0.4 - 0.1)).toFixed(2);
            document.getElementById('input-bcv-rate').value = simulated;
            showToast(`Simulación de Tasa BCV obtenida: Bs. ${simulated}`);
        }

        // --- ADMIN TAB CONTENT GENERATION ---
        function renderAdminTabContent() {
            switch(currentAdminTab) {
                case 'expenses': return renderAdminExpensesTab();
                case 'extraQuotas': return renderAdminExtraQuotasTab();
                case 'payments': return renderAdminPaymentsTab();
                case 'whatsapp': return renderAdminWhatsappTab();
                case 'directPayment': return renderAdminDirectPaymentTab();
                case 'dashboard': return renderAdminDashboardTab();
                case 'suppliers': return renderAdminSuppliersTab();
                case 'reports': return renderAdminReportsTab();
                case 'census': return renderAdminCensusTab();
                case 'settings': return renderAdminSettingsTab();
                default: return renderAdminExpensesTab();
            }
        }

        function renderAdminExpensesTab() {
            const currentPeriodExpenses = appState.expenses.filter(e => e.period === appState.selectedPeriod);
            const totalCommonUSD = currentPeriodExpenses.filter(e => !e.isUncommon).reduce((acc, e) => acc + Number(e.amountUSD), 0);
            const totalUncommonUSD = currentPeriodExpenses.filter(e => e.isUncommon).reduce((acc, e) => acc + Number(e.amountUSD), 0);

            return `
            <div class="space-y-6">
                <!-- Header Control -->
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-4 rounded-xl shadow-sm border border-slate-200">
                    <div>
                        <h1 class="text-xl font-bold text-slate-800">Carga & Distribución de Gastos</h1>
                        <p class="text-xs text-slate-500">Registre facturas de mantenimiento, servicios o gastos no comunes para repartirlos proporcionalmente por alícuota.</p>
                    </div>
                    <div class="flex items-center gap-3">
                        <label class="text-xs font-semibold text-slate-600">Período:</label>
                        <input type="month" value="${appState.selectedPeriod}" onchange="changePeriod(this.value)" class="px-3 py-1.5 border rounded-lg text-xs font-semibold bg-slate-50 focus:ring-2 focus:ring-blue-500">
                    </div>
                </div>

                <!-- Stats summary -->
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center gap-4">
                        <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center text-blue-600">
                            <i data-lucide="receipt" class="w-6 h-6"></i>
                        </div>
                        <div>
                            <p class="text-xs font-medium text-slate-500">Gastos Comunes Totales</p>
                            <h3 class="text-lg font-bold text-slate-800">${formatUSD(totalCommonUSD)}</h3>
                            <p class="text-[10px] text-slate-400">${formatBS(totalCommonUSD * appState.building.bcvRate)}</p>
                        </div>
                    </div>
                    <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center gap-4">
                        <div class="w-12 h-12 bg-amber-100 rounded-xl flex items-center justify-center text-amber-600">
                            <i data-lucide="alert-circle" class="w-6 h-6"></i>
                        </div>
                        <div>
                            <p class="text-xs font-medium text-slate-500">Gastos No Comunes (Específicos)</p>
                            <h3 class="text-lg font-bold text-slate-800">${formatUSD(totalUncommonUSD)}</h3>
                            <p class="text-[10px] text-slate-400">${formatBS(totalUncommonUSD * appState.building.bcvRate)}</p>
                        </div>
                    </div>
                    <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center gap-4">
                        <div class="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center text-emerald-600">
                            <i data-lucide="calculator" class="w-6 h-6"></i>
                        </div>
                        <div>
                            <p class="text-xs font-medium text-slate-500">Total a Facturar Mes</p>
                            <h3 class="text-lg font-bold text-emerald-600">${formatUSD(totalCommonUSD + totalUncommonUSD)}</h3>
                            <p class="text-[10px] text-slate-400">${formatBS((totalCommonUSD + totalUncommonUSD) * appState.building.bcvRate)}</p>
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <!-- Form: Add New Expense -->
                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm h-fit">
                        <h2 class="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
                            <i data-lucide="plus-circle" class="w-4 h-4 text-blue-600"></i> Registrar Nuevo Gasto
                        </h2>
                        <form onsubmit="handleSaveExpense(event)" class="space-y-3">
                            <div>
                                <label class="block text-xs font-medium text-slate-600 mb-1">Descripción del Gasto</label>
                                <input type="text" id="exp-desc" required placeholder="Ej: Reparación de Bomba de Agua" class="w-full px-3 py-1.5 border rounded-lg text-xs focus:ring-2 focus:ring-blue-500">
                            </div>

                            <div class="grid grid-cols-2 gap-2">
                                <div>
                                    <label class="block text-xs font-medium text-slate-600 mb-1">Monto en USD</label>
                                    <input type="number" id="exp-amount" step="0.01" required placeholder="0.00" oninput="updateExpBsPreview()" class="w-full px-3 py-1.5 border rounded-lg text-xs focus:ring-2 focus:ring-blue-500">
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-600 mb-1">Fecha Factura</label>
                                    <input type="date" id="exp-date" required value="${new Date().toISOString().split('T')[0]}" class="w-full px-3 py-1.5 border rounded-lg text-xs focus:ring-2 focus:ring-blue-500">
                                </div>
                            </div>

                            <p id="exp-bs-preview" class="text-[11px] text-blue-600 font-semibold text-right">Equivalente: Bs. 0.00</p>

                            <div class="grid grid-cols-2 gap-2">
                                <div>
                                    <label class="block text-xs font-medium text-slate-600 mb-1">Categoría</label>
                                    <select id="exp-cat" class="w-full px-3 py-1.5 border rounded-lg text-xs focus:ring-2 focus:ring-blue-500">
                                        <option value="Servicios">Servicios Básicos</option>
                                        <option value="Mantenimiento">Mantenimiento</option>
                                        <option value="Reparaciones">Reparaciones</option>
                                        <option value="Honorarios">Honorarios Provisionales</option>
                                        <option value="Otros">Otros Gastos</option>
                                    </select>
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-600 mb-1">Proveedor (Opcional)</label>
                                    <select id="exp-supplier" class="w-full px-3 py-1.5 border rounded-lg text-xs focus:ring-2 focus:ring-blue-500">
                                        <option value="">Seleccione Proveedor</option>
                                        ${appState.suppliers.map(s => `<option value="${s.name}">${s.name}</option>`).join('')}
                                    </select>
                                </div>
                            </div>

                            <!-- Is Special / Uncommon Checkbox -->
                            <div class="pt-2 border-t border-slate-100">
                                <label class="flex items-center gap-2 cursor-pointer">
                                    <input type="checkbox" id="exp-is-uncommon" onchange="toggleUncommonTarget()" class="rounded text-blue-600 focus:ring-blue-500">
                                    <span class="text-xs font-medium text-slate-700">¿Es un Gasto NO Común? (Individual)</span>
                                </label>
                            </div>

                            <div id="uncommon-target-container" class="hidden pl-5">
                                <label class="block text-xs font-medium text-slate-600 mb-1">Cargar Directamente al Apartamento:</label>
                                <select id="exp-target-apt" class="w-full px-3 py-1.5 border rounded-lg text-xs focus:ring-2 focus:ring-blue-500">
                                    ${appState.apartments.map(a => `<option value="${a.id}">Apartamento ${a.id} (${a.owner})</option>`).join('')}
                                </select>
                            </div>

                            <button type="submit" class="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs rounded-lg shadow-sm transition flex items-center justify-center gap-2 mt-4">
                                <i data-lucide="plus" class="w-4 h-4"></i> Guardar y Distribuir
                            </button>
                        </form>
                    </div>

                    <!-- Expenses List for Current Period -->
                    <div class="lg:col-span-2 bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col">
                        <h2 class="text-sm font-bold text-slate-800 mb-4 flex items-center justify-between">
                            <span>Detalle de Facturas Cargadas (${appState.selectedPeriod})</span>
                            <span class="text-xs font-normal text-slate-500">${currentPeriodExpenses.length} registro(s)</span>
                        </h2>

                        <div class="overflow-x-auto custom-scrollbar flex-1">
                            <table class="w-full text-left text-xs">
                                <thead class="bg-slate-50 text-slate-500 uppercase tracking-wider">
                                    <tr>
                                        <th class="p-2.5 rounded-l-md">Descripción</th>
                                        <th class="p-2.5">Tipo</th>
                                        <th class="p-2.5">Monto USD</th>
                                        <th class="p-2.5">Monto Bs</th>
                                        <th class="p-2.5 text-right rounded-r-md">Acciones</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-100">
                                    ${currentPeriodExpenses.length === 0 ? `
                                        <tr>
                                            <td colspan="5" class="p-6 text-center text-slate-400">
                                                No hay gastos registrados para este período.
                                            </td>
                                        </tr>
                                    ` : currentPeriodExpenses.map(exp => `
                                        <tr class="hover:bg-slate-50">
                                            <td class="p-2.5 font-medium text-slate-800">
                                                ${exp.description}
                                                <div class="text-[10px] text-slate-400">${exp.supplier || 'Proveedor N/A'} • ${exp.date}</div>
                                            </td>
                                            <td class="p-2.5">
                                                ${exp.isUncommon ? 
                                                    `<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-700">No Común (Apto ${exp.targetApt})</span>` : 
                                                    `<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-blue-100 text-blue-700">Común (Alícuota)</span>`
                                                }
                                            </td>
                                            <td class="p-2.5 font-bold text-slate-800">${formatUSD(exp.amountUSD)}</td>
                                            <td class="p-2.5 text-slate-500">${formatBS(exp.amountUSD * appState.building.bcvRate)}</td>
                                            <td class="p-2.5 text-right">
                                                <button onclick="deleteExpense('${exp.id}')" class="p-1 text-slate-400 hover:text-rose-600 rounded">
                                                    <i data-lucide="trash-2" class="w-4 h-4"></i>
                                                </button>
                                            </td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            `;
        }

        function changePeriod(val) {
            appState.selectedPeriod = val;
            renderApp();
        }

        function toggleUncommonTarget() {
            const isChecked = document.getElementById('exp-is-uncommon').checked;
            const container = document.getElementById('uncommon-target-container');
            if (isChecked) {
                container.classList.remove('hidden');
            } else {
                container.classList.add('hidden');
            }
        }

        function updateExpBsPreview() {
            const val = parseFloat(document.getElementById('exp-amount').value) || 0;
            const bs = val * appState.building.bcvRate;
            document.getElementById('exp-bs-preview').innerText = `Equivalente: ${formatBS(bs)}`;
        }

        function handleSaveExpense(e) {
            e.preventDefault();
            const desc = document.getElementById('exp-desc').value;
            const amount = parseFloat(document.getElementById('exp-amount').value);
            const date = document.getElementById('exp-date').value;
            const category = document.getElementById('exp-cat').value;
            const supplier = document.getElementById('exp-supplier').value;
            const isUncommon = document.getElementById('exp-is-uncommon').checked;
            const targetApt = isUncommon ? document.getElementById('exp-target-apt').value : 'ALL';

            const newExp = {
                id: 'EXP-' + Date.now().toString().substr(-5),
                period: appState.selectedPeriod,
                description: desc,
                category: category,
                amountUSD: amount,
                isUncommon: isUncommon,
                targetApt: targetApt,
                date: date,
                supplier: supplier
            };

            appState.expenses.push(newExp);
            appState.saveState();
            showToast("Gasto guardado y distribuido correctamente.");
            renderApp();
        }

        function deleteExpense(id) {
            appState.expenses = appState.expenses.filter(e => e.id !== id);
            appState.saveState();
            showToast("Gasto eliminado.", "info");
            renderApp();
        }

        function renderAdminExtraQuotasTab() {
            const currentQuotas = appState.extraQuotas.filter(eq => eq.period === appState.selectedPeriod);

            return `
            <div class="space-y-6">
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-4 rounded-xl shadow-sm border border-slate-200">
                    <div>
                        <h1 class="text-xl font-bold text-slate-800">Cuotas Extraordinarias</h1>
                        <p class="text-xs text-slate-500">Cree fondos especiales o cuotas adicionales repartidas de acuerdo a la alícuota de cada propietario.</p>
                    </div>
                    <div class="flex items-center gap-3">
                        <label class="text-xs font-semibold text-slate-600">Período:</label>
                        <input type="month" value="${appState.selectedPeriod}" onchange="changePeriod(this.value)" class="px-3 py-1.5 border rounded-lg text-xs font-semibold bg-slate-50 focus:ring-2 focus:ring-blue-500">
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <!-- Form: Create Extra Quota -->
                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm h-fit">
                        <h2 class="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
                            <i data-lucide="piggy-bank" class="w-4 h-4 text-blue-600"></i> Nueva Cuota Extraordinaria
                        </h2>
                        <form onsubmit="handleSaveExtraQuota(event)" class="space-y-3">
                            <div>
                                <label class="block text-xs font-medium text-slate-600 mb-1">Título de la Cuota</label>
                                <input type="text" id="eq-title" required placeholder="Ej: Fondo Impermeabilización Roof" class="w-full px-3 py-1.5 border rounded-lg text-xs focus:ring-2 focus:ring-blue-500">
                            </div>

                            <div>
                                <label class="block text-xs font-medium text-slate-600 mb-1">Descripción / Motivo</label>
                                <textarea id="eq-desc" rows="2" placeholder="Detalles de la aprobación en asamblea..." class="w-full px-3 py-1.5 border rounded-lg text-xs focus:ring-2 focus:ring-blue-500"></textarea>
                            </div>

                            <div class="grid grid-cols-2 gap-2">
                                <div>
                                    <label class="block text-xs font-medium text-slate-600 mb-1">Monto Total USD</label>
                                    <input type="number" id="eq-amount" step="0.01" required placeholder="0.00" class="w-full px-3 py-1.5 border rounded-lg text-xs focus:ring-2 focus:ring-blue-500">
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-600 mb-1">Fecha Emisión</label>
                                    <input type="date" id="eq-date" required value="${new Date().toISOString().split('T')[0]}" class="w-full px-3 py-1.5 border rounded-lg text-xs focus:ring-2 focus:ring-blue-500">
                                </div>
                            </div>

                            <button type="submit" class="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs rounded-lg shadow-sm transition flex items-center justify-center gap-2 mt-4">
                                <i data-lucide="plus" class="w-4 h-4"></i> Crear Cuota
                            </button>
                        </form>
                    </div>

                    <!-- Quotas list -->
                    <div class="lg:col-span-2 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <h2 class="text-sm font-bold text-slate-800 mb-4 flex items-center justify-between">
                            <span>Cuotas Extraordinarias Activas (${appState.selectedPeriod})</span>
                        </h2>

                        <div class="space-y-3">
                            ${currentQuotas.length === 0 ? `
                                <div class="p-8 text-center text-slate-400 bg-slate-50 rounded-lg">
                                    No hay cuotas extraordinarias registradas para este mes.
                                </div>
                            ` : currentQuotas.map(eq => `
                                <div class="p-4 rounded-xl border border-slate-200 bg-slate-50/50 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                                    <div>
                                        <div class="flex items-center gap-2">
                                            <h3 class="font-bold text-slate-800 text-sm">${eq.title}</h3>
                                            <span class="text-[10px] bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full font-bold">${eq.date}</span>
                                        </div>
                                        <p class="text-xs text-slate-500 mt-0.5">${eq.description || 'Sin observaciones'}</p>
                                    </div>
                                    <div class="flex items-center gap-4 w-full md:w-auto justify-between border-t md:border-0 pt-2 md:pt-0 border-slate-200">
                                        <div class="text-right">
                                            <p class="text-xs text-slate-400">Total a Distribuir</p>
                                            <p class="font-bold text-slate-800 text-sm">${formatUSD(eq.totalAmountUSD)}</p>
                                        </div>
                                        <button onclick="deleteExtraQuota('${eq.id}')" class="p-2 text-slate-400 hover:text-rose-600 rounded">
                                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                                        </button>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
            `;
        }

        function handleSaveExtraQuota(e) {
            e.preventDefault();
            const title = document.getElementById('eq-title').value;
            const desc = document.getElementById('eq-desc').value;
            const amount = parseFloat(document.getElementById('eq-amount').value);
            const date = document.getElementById('eq-date').value;

            const newEQ = {
                id: 'EQ-' + Date.now().toString().substr(-5),
                period: appState.selectedPeriod,
                title: title,
                description: desc,
                totalAmountUSD: amount,
                date: date
            };

            appState.extraQuotas.push(newEQ);
            appState.saveState();
            showToast("Cuota extraordinaria creada y asignada.");
            renderApp();
        }

        function deleteExtraQuota(id) {
            appState.extraQuotas = appState.extraQuotas.filter(eq => eq.id !== id);
            appState.saveState();
            showToast("Cuota extraordinaria eliminada.", "info");
            renderApp();
        }

        function renderAdminPaymentsTab() {
            const pendingPayments = appState.payments.filter(p => p.status === 'PENDING');
            const historyPayments = appState.payments.filter(p => p.status !== 'PENDING');

            return `
            <div class="space-y-6">
                <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
                    <h1 class="text-xl font-bold text-slate-800">Conciliación de Pagos Reportados</h1>
                    <p class="text-xs text-slate-500">Valide referencias bancarias, pagos móviles o transferencias notificadas por los propietarios para actualizar sus estados de cuenta.</p>
                </div>

                <!-- Section: Pending Approvals -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4">
                    <h2 class="text-sm font-bold text-slate-800 flex items-center gap-2">
                        <i data-lucide="clock" class="w-4 h-4 text-amber-500"></i> Pagos Pendientes por Validar (${pendingPayments.length})
                    </h2>

                    ${pendingPayments.length === 0 ? `
                        <div class="p-8 text-center text-slate-400 bg-slate-50 rounded-lg">
                            <i data-lucide="check-circle-2" class="w-8 h-8 text-emerald-500 mx-auto mb-2 opacity-50"></i>
                            ¡Al día! No hay pagos pendientes por conciliar.
                        </div>
                    ` : `
                        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            ${pendingPayments.map(p => `
                                <div class="p-4 rounded-xl border border-amber-200 bg-amber-50/30 flex flex-col justify-between gap-3 shadow-sm">
                                    <div>
                                        <div class="flex justify-between items-start">
                                            <span class="px-2 py-0.5 rounded bg-blue-600 text-white font-bold text-xs">Apto ${p.aptId}</span>
                                            <span class="text-[10px] text-slate-400">${p.date}</span>
                                        </div>
                                        <div class="mt-2">
                                            <p class="text-lg font-extrabold text-slate-800">${p.currency === 'BS' ? formatBS(p.amountBs) : formatUSD(p.amountUSD)}</p>
                                            <p class="text-[11px] text-slate-500">${p.currency === 'BS' ? `(Equivalente: ${formatUSD(p.amountUSD)} @ Tasa ${p.rateBCV})` : `(Efectivo Divisas)`}</p>
                                        </div>
                                        <div class="mt-2 text-xs space-y-1 text-slate-600">
                                            <p><strong class="text-slate-700">Método:</strong> ${p.method}</p>
                                            <p><strong class="text-slate-700">Ref:</strong> <span class="font-mono bg-white px-1.5 py-0.5 rounded border border-slate-200">${p.reference}</span></p>
                                            ${p.note ? `<p><strong class="text-slate-700">Nota:</strong> ${p.note}</p>` : ''}
                                        </div>
                                    </div>

                                    <div class="flex gap-2 pt-2 border-t border-amber-200/60">
                                        <button onclick="approvePayment('${p.id}')" class="flex-1 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-bold transition flex items-center justify-center gap-1">
                                            <i data-lucide="check" class="w-3.5 h-3.5"></i> Aprobar
                                        </button>
                                        <button onclick="rejectPayment('${p.id}')" class="flex-1 py-1.5 bg-rose-50 hover:bg-rose-100 text-rose-700 rounded-lg text-xs font-bold transition flex items-center justify-center gap-1 border border-rose-200">
                                            <i data-lucide="x" class="w-3.5 h-3.5"></i> Rechazar
                                        </button>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    `}
                </div>

                <!-- Section: Payment History -->
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <h2 class="text-sm font-bold text-slate-800 mb-4">Historial de Pagos Procesados</h2>
                    <div class="overflow-x-auto custom-scrollbar">
                        <table class="w-full text-left text-xs">
                            <thead class="bg-slate-50 text-slate-500 uppercase">
                                <tr>
                                    <th class="p-2.5">Apto</th>
                                    <th class="p-2.5">Fecha</th>
                                    <th class="p-2.5">Método / Ref</th>
                                    <th class="p-2.5">Monto Pagado</th>
                                    <th class="p-2.5">Equiv. USD</th>
                                    <th class="p-2.5">Estado</th>
                                    <th class="p-2.5 text-right">Acción</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-100">
                                ${historyPayments.map(p => `
                                    <tr class="hover:bg-slate-50">
                                        <td class="p-2.5 font-bold text-slate-800">Apto ${p.aptId}</td>
                                        <td class="p-2.5 text-slate-500">${p.date}</td>
                                        <td class="p-2.5">
                                            <span class="font-medium">${p.method}</span>
                                            <div class="text-[10px] text-slate-400 font-mono">Ref: ${p.reference}</div>
                                        </td>
                                        <td class="p-2.5 font-bold">${p.currency === 'BS' ? formatBS(p.amountBs) : formatUSD(p.amountUSD)}</td>
                                        <td class="p-2.5 text-emerald-600 font-semibold">${formatUSD(p.amountUSD)}</td>
                                        <td class="p-2.5">
                                            ${p.status === 'APPROVED' ? 
                                                `<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-700">Aprobado</span>` : 
                                                `<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-100 text-rose-700">Rechazado</span>`
                                            }
                                        </td>
                                        <td class="p-2.5 text-right">
                                            <button onclick="deletePaymentRecord('${p.id}')" title="Eliminar del historial" class="p-1 text-slate-400 hover:text-rose-600 rounded">
                                                <i data-lucide="trash-2" class="w-4 h-4"></i>
                                            </button>
                                        </td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            `;
        }

        function approvePayment(id) {
            const p = appState.payments.find(item => item.id === id);
            if (p) {
                p.status = 'APPROVED';
                appState.saveState();
                showToast(`Pago de Apto ${p.aptId} Aprobado satisfactoriamente.`);
                renderApp();
            }
        }

        function rejectPayment(id) {
            const p = appState.payments.find(item => item.id === id);
            if (p) {
                p.status = 'REJECTED';
                appState.saveState();
                showToast(`Pago de Apto ${p.aptId} ha sido marcado como Rechazado.`, "error");
                renderApp();
            }
        }

        function deletePaymentRecord(id) {
            appState.payments = appState.payments.filter(p => p.id !== id);
            appState.saveState();
            showToast("Registro de pago eliminado.", "info");
            renderApp();
        }

        function renderAdminWhatsappTab() {
            const period = appState.selectedPeriod;
            const expenses = appState.expenses.filter(e => e.period === period);
            const extraQuotas = appState.extraQuotas.filter(eq => eq.period === period);
            const totalCommon = expenses.filter(e => !e.isUncommon).reduce((s, e) => s + Number(e.amountUSD), 0) + 
                               extraQuotas.reduce((s, eq) => s + Number(eq.totalAmountUSD), 0);
            
            // General WhatsApp Text
            let generalText = `*🏢 ${appState.building.name.toUpperCase()}*\n`;
            generalText += `*AVISO DE COBRO - PERÍODO: ${period}*\n`;
            generalText += `*Tasa Oficial BCV:* Bs. ${appState.building.bcvRate.toFixed(2)}\n`;
            generalText += `------------------------------------\n`;
            generalText += `*DESGLOSE DE GASTOS COMUNES Y CUOTAS:*\n`;
            
            expenses.filter(e => !e.isUncommon).forEach(e => {
                generalText += `• ${e.description}: $${Number(e.amountUSD).toFixed(2)}\n`;
            });
            extraQuotas.forEach(eq => {
                generalText += `• [Cuota Extra] ${eq.title}: $${Number(eq.totalAmountUSD).toFixed(2)}\n`;
            });

            generalText += `------------------------------------\n`;
            generalText += `*TOTAL GASTOS COMUNES:* $${totalCommon.toFixed(2)} (Bs. ${(totalCommon * appState.building.bcvRate).toFixed(2)})\n\n`;
            generalText += `Por favor consultar su aviso individual o ingresar al sistema para el reporte de pago. ¡Muchas gracias!`;

            return `
            <div class="space-y-6">
                <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
                    <h1 class="text-xl font-bold text-slate-800">Envío Masivo & Avisos por WhatsApp</h1>
                    <p class="text-xs text-slate-500">Genere automáticamente los mensajes formateados para el grupo general de condominio o avisos individuales por apartamento.</p>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <!-- General Message -->
                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-3">
                        <div class="flex justify-between items-center">
                            <h2 class="text-sm font-bold text-slate-800 flex items-center gap-2">
                                <i data-lucide="message-square" class="w-4 h-4 text-emerald-600"></i> Resumen General del Mes (${period})
                            </h2>
                            <button onclick="copyToClipboard('wa-general-text')" class="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 rounded text-xs text-slate-700 font-medium flex items-center gap-1">
                                <i data-lucide="copy" class="w-3.5 h-3.5"></i> Copiar Texto
                            </button>
                        </div>
                        <textarea id="wa-general-text" rows="12" class="w-full p-3 bg-slate-50 font-mono text-xs border rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500">${generalText}</textarea>
                    </div>

                    <!-- Individual Message Generator -->
                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4">
                        <h2 class="text-sm font-bold text-slate-800 flex items-center gap-2">
                            <i data-lucide="user-check" class="w-4 h-4 text-blue-600"></i> Generador de Mensaje Individual
                        </h2>

                        <div>
                            <label class="block text-xs font-semibold text-slate-600 mb-1">Seleccionar Apartamento</label>
                            <select id="wa-apt-select" onchange="generateIndividualWaText()" class="w-full px-3 py-2 border rounded-lg text-xs bg-slate-50">
                                ${appState.apartments.map(a => `<option value="${a.id}">Apartamento ${a.id} - ${a.owner}</option>`).join('')}
                            </select>
                        </div>

                        <textarea id="wa-individual-text" rows="8" class="w-full p-3 bg-slate-50 font-mono text-xs border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>

                        <div class="flex gap-2">
                            <button onclick="copyToClipboard('wa-individual-text')" class="flex-1 py-2 bg-slate-200 hover:bg-slate-300 rounded-lg text-xs font-semibold text-slate-700 flex items-center justify-center gap-1">
                                <i data-lucide="copy" class="w-3.5 h-3.5"></i> Copiar
                            </button>
                            <button onclick="sendWaDirect()" class="flex-1 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-bold flex items-center justify-center gap-1">
                                <i data-lucide="send" class="w-3.5 h-3.5"></i> Abrir en WhatsApp
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            `;
        }

        function generateIndividualWaText() {
            const select = document.getElementById('wa-apt-select');
            if (!select) return;
            const aptId = select.value;
            const period = appState.selectedPeriod;
            const bill = calculateAptBill(aptId, period);

            let txt = `*🏢 ${appState.building.name}*\n`;
            txt += `*Estimado(a) ${bill.apt.owner} (Apto ${aptId})*\n\n`;
            txt += `Le enviamos el resumen de su aviso de cobro para el mes *${period}*:\n`;
            txt += `• Alícuota: ${bill.apt.alicuota}%\n`;
            txt += `• Gastos Comunes + Extra: $${(bill.aptCommonUSD + bill.aptExtraUSD).toFixed(2)}\n`;
            if (bill.aptUncommonUSD > 0) {
                txt += `• Gastos No Comunes Apto: $${bill.aptUncommonUSD.toFixed(2)}\n`;
            }
            txt += `------------------------------------\n`;
            txt += `*TOTAL A CANCELAR:* $${bill.totalUSD.toFixed(2)}\n`;
            txt += `*TOTAL EN BOLÍVARES (Tasa BCV ${bill.rateBCV}):* Bs. ${bill.totalBS.toFixed(2)}\n\n`;
            txt += `Recuerde reportar su transferencia o pago móvil a la brevedad. ¡Gracias!`;

            document.getElementById('wa-individual-text').value = txt;
        }

        function sendWaDirect() {
            const aptId = document.getElementById('wa-apt-select').value;
            const apt = appState.apartments.find(a => a.id === aptId);
            const text = encodeURIComponent(document.getElementById('wa-individual-text').value);
            const phone = apt ? apt.phone.replace(/[^0-9]/g, '') : '';
            window.open(`https://wa.me/${phone}?text=${text}`, '_blank');
        }

        function copyToClipboard(elementId) {
            const copyText = document.getElementById(elementId);
            copyText.select();
            document.execCommand('copy');
            showToast("Texto copiado al portapapeles.");
        }

        function renderAdminDirectPaymentTab() {
            return `
            <div class="max-w-2xl mx-auto space-y-6">
                <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
                    <h1 class="text-xl font-bold text-slate-800 flex items-center gap-2">
                        <i data-lucide="plus-circle" class="w-5 h-5 text-blue-600"></i> Registrar Pago Directo
                    </h1>
                    <p class="text-xs text-slate-500 mt-1">Módulo especial para que el administrador registre manualmente el pago de vecinos que no sepan o no puedan ingresarlo al sistema.</p>

                    <form onsubmit="handleDirectPaymentSave(event)" class="mt-6 space-y-4">
                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Apartamento Propietario</label>
                                <select id="dp-apt" class="w-full px-3 py-2 border rounded-lg text-xs bg-slate-50 focus:ring-2 focus:ring-blue-500">
                                    ${appState.apartments.map(a => `<option value="${a.id}">Apartamento ${a.id} (${a.owner})</option>`).join('')}
                                </select>
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Período que Cancela</label>
                                <input type="month" id="dp-period" value="${appState.selectedPeriod}" class="w-full px-3 py-2 border rounded-lg text-xs bg-slate-50">
                            </div>
                        </div>

                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Moneda del Pago</label>
                                <select id="dp-currency" onchange="toggleDpCurrency()" class="w-full px-3 py-2 border rounded-lg text-xs bg-slate-50">
                                    <option value="BS">Bolívares (Bs)</option>
                                    <option value="USD">Dólares (USD / Divisas)</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Método de Pago</label>
                                <select id="dp-method" class="w-full px-3 py-2 border rounded-lg text-xs bg-slate-50">
                                    <option value="Pago Móvil">Pago Móvil</option>
                                    <option value="Transferencia">Transferencia Bancaria</option>
                                    <option value="Efectivo USD">Efectivo Divisas</option>
                                    <option value="Depósito">Depósito Bancario</option>
                                </select>
                            </div>
                        </div>

                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Monto Cancelado</label>
                                <input type="number" id="dp-amount" step="0.01" required placeholder="0.00" oninput="updateDpConversion()" class="w-full px-3 py-2 border rounded-lg text-xs">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Referencia / Comprobante</label>
                                <input type="text" id="dp-ref" required placeholder="Ej: 88776612" class="w-full px-3 py-2 border rounded-lg text-xs">
                            </div>
                        </div>

                        <div class="p-3 bg-blue-50 rounded-lg text-xs text-blue-800 space-y-1">
                            <p class="font-bold flex justify-between">
                                <span>Tasa Oficial BCV Aplicada:</span>
                                <span>Bs. ${appState.building.bcvRate.toFixed(2)}</span>
                            </p>
                            <p id="dp-calc-preview" class="text-right font-semibold text-blue-600">Equivalente USD: $0.00</p>
                        </div>

                        <div>
                            <label class="block text-xs font-semibold text-slate-600 mb-1">Observaciones / Nota del Admin</label>
                            <input type="text" id="dp-note" placeholder="Ej: Pago entregado en efectivo en conserjería" class="w-full px-3 py-2 border rounded-lg text-xs">
                        </div>

                        <button type="submit" class="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-lg shadow-sm transition">
                            Registrar y Aprobar Pago Inmediatamente
                        </button>
                    </form>
                </div>
            </div>
            `;
        }

        function toggleDpCurrency() {
            updateDpConversion();
        }

        function updateDpConversion() {
            const currency = document.getElementById('dp-currency').value;
            const amount = parseFloat(document.getElementById('dp-amount').value) || 0;
            const preview = document.getElementById('dp-calc-preview');

            if (currency === 'BS') {
                const usd = amount / appState.building.bcvRate;
                preview.innerText = `Equivalente en USD: $${usd.toFixed(2)}`;
            } else {
                const bs = amount * appState.building.bcvRate;
                preview.innerText = `Equivalente en Bolívares: Bs. ${bs.toFixed(2)}`;
            }
        }

        function handleDirectPaymentSave(e) {
            e.preventDefault();
            const aptId = document.getElementById('dp-apt').value;
            const period = document.getElementById('dp-period').value;
            const currency = document.getElementById('dp-currency').value;
            const method = document.getElementById('dp-method').value;
            const rawAmount = parseFloat(document.getElementById('dp-amount').value);
            const ref = document.getElementById('dp-ref').value;
            const note = document.getElementById('dp-note').value;

            let amountUSD = 0;
            let amountBs = 0;

            if (currency === 'BS') {
                amountBs = rawAmount;
                amountUSD = rawAmount / appState.building.bcvRate;
            } else {
                amountUSD = rawAmount;
                amountBs = rawAmount * appState.building.bcvRate;
            }

            const newPayment = {
                id: 'PAY-' + Date.now().toString().substr(-5),
                aptId: aptId,
                period: period,
                amountUSD: amountUSD,
                amountBs: amountBs,
                rateBCV: appState.building.bcvRate,
                currency: currency,
                method: method,
                reference: ref,
                date: new Date().toISOString().split('T')[0],
                status: 'APPROVED',
                note: note || 'Registrado por Administrador'
            };

            appState.payments.push(newPayment);
            appState.saveState();
            showToast(`Pago de Apto ${aptId} registrado y acreditado.`);
            switchAdminTab('payments');
        }

        function renderAdminDashboardTab() {
            // Calculate balances for all apartments
            const aptSummaries = appState.apartments.map(a => {
                const bal = calculateAptBalance(a.id);
                return {
                    apt: a,
                    ...bal
                };
            });

            const debtors = aptSummaries.filter(s => s.balanceUSD < -0.01);
            const totalDebtsUSD = debtors.reduce((sum, d) => sum + Math.abs(d.balanceUSD), 0);
            
            // Total Income vs Expenses for 2026-02
            const periodExpenses = appState.expenses.filter(e => e.period === appState.selectedPeriod).reduce((s, e) => s + Number(e.amountUSD), 0);
            const periodIncome = appState.payments.filter(p => p.period === appState.selectedPeriod && p.status === 'APPROVED').reduce((s, p) => s + Number(p.amountUSD), 0);

            setTimeout(() => renderDashboardCharts(debtors, periodIncome, periodExpenses), 100);

            return `
            <div class="space-y-6">
                <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
                    <h1 class="text-xl font-bold text-slate-800">Morosidad & Balance Financiero</h1>
                    <p class="text-xs text-slate-500">Panel de control con antigüedad de deuda, lista de propietarios morosos y relación Ingresos vs. Egresos.</p>
                </div>

                <!-- KPI Cards -->
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div class="bg-white p-4 rounded-xl border border-rose-200 shadow-sm flex items-center justify-between">
                        <div>
                            <p class="text-xs font-medium text-slate-500">Monto Total Morosidad</p>
                            <h3 class="text-xl font-extrabold text-rose-600">${formatUSD(totalDebtsUSD)}</h3>
                            <p class="text-[10px] text-slate-400">${formatBS(totalDebtsUSD * appState.building.bcvRate)}</p>
                        </div>
                        <div class="w-10 h-10 bg-rose-100 rounded-lg flex items-center justify-center text-rose-600">
                            <i data-lucide="alert-triangle" class="w-5 h-5"></i>
                        </div>
                    </div>

                    <div class="bg-white p-4 rounded-xl border border-emerald-200 shadow-sm flex items-center justify-between">
                        <div>
                            <p class="text-xs font-medium text-slate-500">Recaudado este Mes (${appState.selectedPeriod})</p>
                            <h3 class="text-xl font-extrabold text-emerald-600">${formatUSD(periodIncome)}</h3>
                            <p class="text-[10px] text-slate-400">${formatBS(periodIncome * appState.building.bcvRate)}</p>
                        </div>
                        <div class="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center text-emerald-600">
                            <i data-lucide="trending-up" class="w-5 h-5"></i>
                        </div>
                    </div>

                    <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                        <div>
                            <p class="text-xs font-medium text-slate-500">Egresos / Facturas Mes</p>
                            <h3 class="text-xl font-extrabold text-slate-800">${formatUSD(periodExpenses)}</h3>
                            <p class="text-[10px] text-slate-400">${formatBS(periodExpenses * appState.building.bcvRate)}</p>
                        </div>
                        <div class="w-10 h-10 bg-slate-100 rounded-lg flex items-center justify-center text-slate-600">
                            <i data-lucide="trending-down" class="w-5 h-5"></i>
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <!-- Debtors Table -->
                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <h2 class="text-sm font-bold text-slate-800 mb-4 flex items-center justify-between">
                            <span class="flex items-center gap-2">
                                <i data-lucide="users" class="w-4 h-4 text-rose-600"></i> Lista de Morosos (${debtors.length})
                            </span>
                        </h2>

                        <div class="overflow-x-auto custom-scrollbar">
                            <table class="w-full text-left text-xs">
                                <thead class="bg-slate-50 text-slate-500 uppercase">
                                    <tr>
                                        <th class="p-2.5">Apto</th>
                                        <th class="p-2.5">Propietario</th>
                                        <th class="p-2.5">Deuda USD</th>
                                        <th class="p-2.5">Deuda Bs</th>
                                        <th class="p-2.5">Acción</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-100">
                                    ${debtors.length === 0 ? `
                                        <tr>
                                            <td colspan="5" class="p-6 text-center text-emerald-600 font-semibold">
                                                ¡Excelente! No hay apartamentos con morosidad.
                                            </td>
                                        </tr>
                                    ` : debtors.map(d => `
                                        <tr class="hover:bg-slate-50">
                                            <td class="p-2.5 font-bold text-slate-800">Apto ${d.apt.id}</td>
                                            <td class="p-2.5">${d.apt.owner}</td>
                                            <td class="p-2.5 font-bold text-rose-600">${formatUSD(Math.abs(d.balanceUSD))}</td>
                                            <td class="p-2.5 text-slate-500">${formatBS(Math.abs(d.balanceUSD) * appState.building.bcvRate)}</td>
                                            <td class="p-2.5">
                                                <button onclick="switchAdminTab('whatsapp')" class="px-2 py-1 bg-emerald-100 hover:bg-emerald-200 text-emerald-700 rounded text-[10px] font-bold">
                                                    Recordar
                                                </button>
                                            </td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Chart Container -->
                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col items-center justify-center">
                        <h2 class="text-sm font-bold text-slate-800 mb-2 w-full text-left">Balance de Flujo (Ingresos vs Egresos)</h2>
                        <div class="w-full max-w-xs h-60">
                            <canvas id="finance-chart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
            `;
        }

        function renderDashboardCharts(debtors, income, expenses) {
            const ctx = document.getElementById('finance-chart');
            if (!ctx) return;

            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Ingresos Cobrados', 'Egresos Facturados'],
                    datasets: [{
                        data: [income, expenses],
                        backgroundColor: ['#10b981', '#f43f5e']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'bottom' }
                    }
                }
            });
        }

        function renderAdminSuppliersTab() {
            return `
            <div class="space-y-6">
                <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
                    <h1 class="text-xl font-bold text-slate-800">Registro de Proveedores</h1>
                    <p class="text-xs text-slate-500">Directorio de contratistas y proveedores recurrentes para vincular sus facturas y consultar historiales.</p>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <!-- New Supplier Form -->
                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm h-fit">
                        <h2 class="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
                            <i data-lucide="plus-circle" class="w-4 h-4 text-blue-600"></i> Registrar Proveedor
                        </h2>
                        <form onsubmit="handleSaveSupplier(event)" class="space-y-3">
                            <div>
                                <label class="block text-xs font-medium text-slate-600 mb-1">Nombre / Razón Social</label>
                                <input type="text" id="sup-name" required placeholder="Ej: MultiServicios C.A." class="w-full px-3 py-1.5 border rounded-lg text-xs">
                            </div>
                            <div>
                                <label class="block text-xs font-medium text-slate-600 mb-1">RIF / Identificación Fiscal</label>
                                <input type="text" id="sup-rif" required placeholder="J-12345678-0" class="w-full px-3 py-1.5 border rounded-lg text-xs">
                            </div>
                            <div>
                                <label class="block text-xs font-medium text-slate-600 mb-1">Servicio que presta</label>
                                <input type="text" id="sup-service" required placeholder="Ej: Cerrajería, Ascensores" class="w-full px-3 py-1.5 border rounded-lg text-xs">
                            </div>
                            <div class="grid grid-cols-2 gap-2">
                                <div>
                                    <label class="block text-xs font-medium text-slate-600 mb-1">Teléfono</label>
                                    <input type="text" id="sup-phone" placeholder="0414-1234567" class="w-full px-3 py-1.5 border rounded-lg text-xs">
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-600 mb-1">Correo electrónico</label>
                                    <input type="email" id="sup-email" placeholder="correo@proveedor.com" class="w-full px-3 py-1.5 border rounded-lg text-xs">
                                </div>
                            </div>
                            <button type="submit" class="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs rounded-lg shadow-sm transition mt-2">
                                Guardar Proveedor
                            </button>
                        </form>
                    </div>

                    <!-- Suppliers Directory Table -->
                    <div class="lg:col-span-2 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <h2 class="text-sm font-bold text-slate-800 mb-4">Directorio de Contratistas Registrados</h2>
                        <div class="overflow-x-auto custom-scrollbar">
                            <table class="w-full text-left text-xs">
                                <thead class="bg-slate-50 text-slate-500 uppercase">
                                    <tr>
                                        <th class="p-2.5">Proveedor</th>
                                        <th class="p-2.5">RIF</th>
                                        <th class="p-2.5">Servicio</th>
                                        <th class="p-2.5">Contacto</th>
                                        <th class="p-2.5 text-right">Acción</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-100">
                                    ${appState.suppliers.map(s => `
                                        <tr class="hover:bg-slate-50">
                                            <td class="p-2.5 font-bold text-slate-800">${s.name}</td>
                                            <td class="p-2.5 font-mono text-slate-500">${s.rif}</td>
                                            <td class="p-2.5"><span class="px-2 py-0.5 rounded bg-blue-50 text-blue-700 font-medium">${s.service}</span></td>
                                            <td class="p-2.5 text-slate-600">${s.phone}<br><span class="text-[10px] text-slate-400">${s.email}</span></td>
                                            <td class="p-2.5 text-right">
                                                <button onclick="deleteSupplier('${s.id}')" class="p-1 text-slate-400 hover:text-rose-600 rounded">
                                                    <i data-lucide="trash-2" class="w-4 h-4"></i>
                                                </button>
                                            </td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            `;
        }

        function handleSaveSupplier(e) {
            e.preventDefault();
            const newSup = {
                id: 'SUP-' + Date.now().toString().substr(-5),
                name: document.getElementById('sup-name').value,
                rif: document.getElementById('sup-rif').value,
                service: document.getElementById('sup-service').value,
                phone: document.getElementById('sup-phone').value,
                email: document.getElementById('sup-email').value
            };

            appState.suppliers.push(newSup);
            appState.saveState();
            showToast("Proveedor registrado con éxito.");
            renderApp();
        }

        function deleteSupplier(id) {
            appState.suppliers = appState.suppliers.filter(s => s.id !== id);
            appState.saveState();
            showToast("Proveedor eliminado.", "info");
            renderApp();
        }

        let currentReportType = 'suppliers';

        function renderAdminReportsTab() {
            return `
            <div class="space-y-6">
                <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                    <div>
                        <h1 class="text-xl font-bold text-slate-800">Reportes Generales de Gestión</h1>
                        <p class="text-xs text-slate-500">Módulo de generación e impresión de reportes para entregas de cuenta anuales o periódicas.</p>
                    </div>
                    <button onclick="window.print()" class="px-3 py-2 bg-slate-800 hover:bg-slate-900 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 no-print">
                        <i data-lucide="printer" class="w-4 h-4"></i> Imprimir Reporte
                    </button>
                </div>

                <!-- Report Selector Tabs -->
                <div class="flex rounded-lg bg-white p-1 shadow-sm border border-slate-200 no-print">
                    <button onclick="switchReportType('suppliers')" class="flex-1 py-2 text-xs font-semibold rounded-md ${currentReportType === 'suppliers' ? 'bg-blue-600 text-white' : 'text-slate-600 hover:bg-slate-50'}">
                        1. Reporte de Proveedores
                    </button>
                    <button onclick="switchReportType('owners')" class="flex-1 py-2 text-xs font-semibold rounded-md ${currentReportType === 'owners' ? 'bg-blue-600 text-white' : 'text-slate-600 hover:bg-slate-50'}">
                        2. Propietarios / Alícuota Mensual
                    </button>
                    <button onclick="switchReportType('extraQuotas')" class="flex-1 py-2 text-xs font-semibold rounded-md ${currentReportType === 'extraQuotas' ? 'bg-blue-600 text-white' : 'text-slate-600 hover:bg-slate-50'}">
                        3. Reporte Cuotas Extraordinarias
                    </button>
                </div>

                <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm min-h-[400px]">
                    ${renderReportContent()}
                </div>
            </div>
            `;
        }

        function switchReportType(type) {
            currentReportType = type;
            renderApp();
        }

        function renderReportContent() {
            if (currentReportType === 'suppliers') {
                return `
                <div class="space-y-4">
                    <div class="border-b pb-3">
                        <h2 class="text-base font-bold text-slate-800">Reporte de Pagos a Proveedores</h2>
                        <p class="text-xs text-slate-500">Detalle de montos cancelados por concepto de servicios y contratos.</p>
                    </div>
                    <table class="w-full text-left text-xs border-collapse">
                        <thead>
                            <tr class="bg-slate-100 text-slate-700 font-bold border-b">
                                <th class="p-2">Proveedor</th>
                                <th class="p-2">Monto Cancelado (USD)</th>
                                <th class="p-2">Equiv. Bs.</th>
                                <th class="p-2">Mes / Año</th>
                                <th class="p-2">Observación</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                            ${appState.expenses.map(e => `
                                <tr>
                                    <td class="p-2 font-semibold">${e.supplier || 'N/A'}</td>
                                    <td class="p-2 font-bold">${formatUSD(e.amountUSD)}</td>
                                    <td class="p-2">${formatBS(e.amountUSD * appState.building.bcvRate)}</td>
                                    <td class="p-2">${e.period}</td>
                                    <td class="p-2 text-slate-500">${e.description}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
                `;
            } else if (currentReportType === 'owners') {
                return `
                <div class="space-y-4">
                    <div class="border-b pb-3">
                        <h2 class="text-base font-bold text-slate-800">Reporte Propietarios - Alícuotas y Saldos</h2>
                        <p class="text-xs text-slate-500">Estado de cuenta global por alícuotas del condominio.</p>
                    </div>
                    <table class="w-full text-left text-xs border-collapse">
                        <thead>
                            <tr class="bg-slate-100 text-slate-700 font-bold border-b">
                                <th class="p-2">ID Apto</th>
                                <th class="p-2">Propietario</th>
                                <th class="p-2">Alícuota</th>
                                <th class="p-2">Facturado Acumulado</th>
                                <th class="p-2">Pagado Acumulado</th>
                                <th class="p-2">Saldo (Deudor / A favor)</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                            ${appState.apartments.map(a => {
                                const bal = calculateAptBalance(a.id);
                                return `
                                <tr>
                                    <td class="p-2 font-bold">Apto ${a.id}</td>
                                    <td class="p-2">${a.owner}</td>
                                    <td class="p-2 font-semibold">${a.alicuota}%</td>
                                    <td class="p-2">${formatUSD(bal.billedUSD)}</td>
                                    <td class="p-2">${formatUSD(bal.paidUSD)}</td>
                                    <td class="p-2 font-bold ${bal.balanceUSD < -0.01 ? 'text-rose-600' : 'text-emerald-600'}">
                                        ${bal.balanceUSD < -0.01 ? `Deudor: ${formatUSD(Math.abs(bal.balanceUSD))}` : `A favor: ${formatUSD(bal.balanceUSD)}`}
                                    </td>
                                </tr>
                                `;
                            }).join('')}
                        </tbody>
                    </table>
                </div>
                `;
            } else if (currentReportType === 'extraQuotas') {
                return `
                <div class="space-y-4">
                    <div class="border-b pb-3">
                        <h2 class="text-base font-bold text-slate-800">Reporte de Cuotas Extraordinarias</h2>
                        <p class="text-xs text-slate-500">Histórico de aportes extraordinarios por apartamento.</p>
                    </div>
                    <table class="w-full text-left text-xs border-collapse">
                        <thead>
                            <tr class="bg-slate-100 text-slate-700 font-bold border-b">
                                <th class="p-2">ID Apto</th>
                                <th class="p-2">Alícuota</th>
                                <th class="p-2">Cuota Titulo</th>
                                <th class="p-2">Monto Alícuota (USD)</th>
                                <th class="p-2">Fecha</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                            ${appState.apartments.flatMap(a => 
                                appState.extraQuotas.map(eq => `
                                    <tr>
                                        <td class="p-2 font-bold">Apto ${a.id}</td>
                                        <td class="p-2">${a.alicuota}%</td>
                                        <td class="p-2 font-medium">${eq.title}</td>
                                        <td class="p-2 font-bold text-slate-800">${formatUSD((eq.totalAmountUSD * a.alicuota)/100)}</td>
                                        <td class="p-2 text-slate-500">${eq.date}</td>
                                    </tr>
                                `)
                            ).join('')}
                        </tbody>
                    </table>
                </div>
                `;
            }
        }

        function renderAdminCensusTab() {
            const totalAlicuota = appState.apartments.reduce((sum, a) => sum + Number(a.alicuota), 0);

            return `
            <div class="space-y-6">
                <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200 flex justify-between items-center">
                    <div>
                        <h1 class="text-xl font-bold text-slate-800">Censo de Propietarios y Alícuotas</h1>
                        <p class="text-xs text-slate-500">Padrón oficial de 13 apartamentos con distribución paramétrica exacta de alícuotas (Sumatoria = 100%).</p>
                    </div>
                    <div class="text-right">
                        <span class="text-xs text-slate-500">Suma Total Alicuotas:</span>
                        <div class="text-lg font-extrabold ${totalAlicuota === 100 ? 'text-emerald-600' : 'text-rose-600'}">${totalAlicuota}%</div>
                    </div>
                </div>

                <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                    <div class="overflow-x-auto custom-scrollbar">
                        <table class="w-full text-left text-xs">
                            <thead class="bg-slate-50 text-slate-500 uppercase">
                                <tr>
                                    <th class="p-3">Apartamento</th>
                                    <th class="p-3">Propietario / Razón Social</th>
                                    <th class="p-3">Teléfono (WhatsApp)</th>
                                    <th class="p-3">Alícuota Estape</th>
                                    <th class="p-3">Gestión Contraseña</th>
                                    <th class="p-3 text-right">Acción</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-100">
                                ${appState.apartments.map(a => `
                                    <tr class="hover:bg-slate-50">
                                        <td class="p-3 font-extrabold text-slate-800">
                                            <span class="px-2 py-1 bg-slate-100 rounded text-blue-700">Apto ${a.id}</span>
                                        </td>
                                        <td class="p-3 font-medium">${a.owner}</td>
                                        <td class="p-3 font-mono text-slate-600">${a.phone}</td>
                                        <td class="p-3 font-bold text-slate-800">${a.alicuota}%</td>
                                        <td class="p-3">
                                            <button onclick="promptResetPassword('${a.id}')" class="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded text-[11px] font-medium flex items-center gap-1">
                                                <i data-lucide="key" class="w-3 h-3"></i> Reset Pass
                                            </button>
                                        </td>
                                        <td class="p-3 text-right">
                                            <button onclick="promptEditOwner('${a.id}')" class="p-1.5 text-blue-600 hover:bg-blue-50 rounded">
                                                <i data-lucide="edit-3" class="w-4 h-4"></i>
                                            </button>
                                        </td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            `;
        }

        function promptResetPassword(aptId) {
            const newPwd = prompt(`Ingrese la nueva contraseña para el Propietario del Apto ${aptId}:`, "123456");
            if (newPwd) {
                appState.resetPassword(aptId, newPwd);
                showToast(`Contraseña del Apto ${aptId} reseteada correctamente.`);
            }
        }

        function promptEditOwner(aptId) {
            const apt = appState.apartments.find(a => a.id === aptId);
            if (!apt) return;
            const newName = prompt(`Nombre del propietario para Apto ${aptId}:`, apt.owner);
            const newPhone = prompt(`Teléfono de contacto para Apto ${aptId}:`, apt.phone);

            if (newName) apt.owner = newName;
            if (newPhone) apt.phone = newPhone;

            appState.saveState();
            showToast("Datos de propietario actualizados.");
            renderApp();
        }

        function renderAdminSettingsTab() {
            return `
            <div class="max-w-2xl mx-auto space-y-6">
                <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
                    <h1 class="text-xl font-bold text-slate-800">Configuración del Edificio / Condominio</h1>
                    <p class="text-xs text-slate-500 mt-1">Personalice los datos legales, dirección e imagen del condominio que aparecerán en todos los recibos y comprobantes.</p>

                    <form onsubmit="handleSaveBuildingSettings(event)" class="mt-6 space-y-4">
                        <div>
                            <label class="block text-xs font-semibold text-slate-600 mb-1">Nombre del Condominio / Edificio</label>
                            <input type="text" id="set-name" value="${appState.building.name}" required class="w-full px-3 py-2 border rounded-lg text-xs">
                        </div>

                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">RIF Legal</label>
                                <input type="text" id="set-rif" value="${appState.building.rif}" required class="w-full px-3 py-2 border rounded-lg text-xs">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">URL Logo del Edificio</label>
                                <input type="text" id="set-logo" value="${appState.building.logoUrl}" required class="w-full px-3 py-2 border rounded-lg text-xs">
                            </div>
                        </div>

                        <div>
                            <label class="block text-xs font-semibold text-slate-600 mb-1">Dirección Física y Legal</label>
                            <textarea id="set-address" rows="2" class="w-full px-3 py-2 border rounded-lg text-xs">${appState.building.address}</textarea>
                        </div>

                        <button type="submit" class="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-lg shadow-sm transition">
                            Guardar Cambios de Configuración
                        </button>
                    </form>
                </div>
            </div>
            `;
        }

        function handleSaveBuildingSettings(e) {
            e.preventDefault();
            appState.building.name = document.getElementById('set-name').value;
            appState.building.rif = document.getElementById('set-rif').value;
            appState.building.logoUrl = document.getElementById('set-logo').value;
            appState.building.address = document.getElementById('set-address').value;

            appState.saveState();
            showToast("Datos del Condominio actualizados.");
            renderApp();
        }

        let currentOwnerTab = 'bill'; // 'bill', 'pay', 'statement'

        function renderOwnerLayout() {
            const aptId = appState.currentUser.aptId;
            const apt = appState.apartments.find(a => a.id === aptId);
            const bill = calculateAptBill(aptId, appState.selectedPeriod);
            const balance = calculateAptBalance(aptId);

            return `
            <div class="min-h-screen bg-slate-100 flex flex-col">
                <!-- Top Navigation Header -->
                <header class="bg-slate-900 text-white shadow-md no-print">
                    <div class="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
                        <div class="flex items-center gap-3">
                            <img src="${appState.building.logoUrl}" class="w-9 h-9 rounded-lg object-cover bg-white p-0.5" alt="Logo">
                            <div>
                                <h1 class="text-sm font-bold leading-tight">${appState.building.name}</h1>
                                <p class="text-[10px] text-blue-400 font-mono">Apartamento ${aptId} • ${apt ? apt.owner : ''}</p>
                            </div>
                        </div>
                        <div class="flex items-center gap-3">
                            <span class="text-xs bg-slate-800 px-2.5 py-1 rounded-md text-emerald-400 font-bold border border-slate-700">
                                BCV: Bs. ${appState.building.bcvRate.toFixed(2)}
                            </span>
                            <button onclick="appState.logout()" title="Cerrar Sesión" class="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded">
                                <i data-lucide="log-out" class="w-4 h-4"></i>
                            </button>
                        </div>
                    </div>
                </header>

                <!-- Sub-nav Navigation Pills -->
                <div class="bg-white border-b border-slate-200 no-print">
                    <div class="max-w-5xl mx-auto px-4 flex gap-2 py-2 text-xs font-semibold">
                        <button onclick="switchOwnerTab('bill')" class="px-4 py-2 rounded-lg transition ${currentOwnerTab === 'bill' ? 'bg-blue-600 text-white' : 'text-slate-600 hover:bg-slate-100'}">
                            <i data-lucide="file-text" class="w-3.5 h-3.5 inline mr-1"></i> Recibo del Mes
                        </button>
                        <button onclick="switchOwnerTab('pay')" class="px-4 py-2 rounded-lg transition ${currentOwnerTab === 'pay' ? 'bg-blue-600 text-white' : 'text-slate-600 hover:bg-slate-100'}">
                            <i data-lucide="send" class="w-3.5 h-3.5 inline mr-1"></i> Reportar Pago
                        </button>
                        <button onclick="switchOwnerTab('statement')" class="px-4 py-2 rounded-lg transition ${currentOwnerTab === 'statement' ? 'bg-blue-600 text-white' : 'text-slate-600 hover:bg-slate-100'}">
                            <i data-lucide="history" class="w-3.5 h-3.5 inline mr-1"></i> Estado de Cuenta
                        </button>
                    </div>
                </div>

                <!-- Main Content Body -->
                <main class="max-w-5xl mx-auto w-full p-4 md:p-6 flex-1">
                    ${renderOwnerTabContent(aptId, bill, balance)}
                </main>
            </div>
            `;
        }

        function switchOwnerTab(tab) {
            currentOwnerTab = tab;
            renderApp();
        }

        function renderOwnerTabContent(aptId, bill, balance) {
            if (currentOwnerTab === 'bill') {
                const commonExpenses = appState.expenses.filter(e => e.period === appState.selectedPeriod && !e.isUncommon);
                const extraQuotas = appState.extraQuotas.filter(eq => eq.period === appState.selectedPeriod);
                const uncommonExpenses = appState.expenses.filter(e => e.period === appState.selectedPeriod && e.isUncommon && e.targetApt === aptId);

                return `
                <div class="space-y-6">
                    <!-- Period Filter & Print -->
                    <div class="flex justify-between items-center bg-white p-4 rounded-xl shadow-sm border border-slate-200 no-print">
                        <div class="flex items-center gap-2">
                            <label class="text-xs font-semibold text-slate-600">Período de Cobro:</label>
                            <input type="month" value="${appState.selectedPeriod}" onchange="changePeriod(this.value)" class="px-3 py-1.5 border rounded-lg text-xs font-semibold bg-slate-50">
                        </div>
                        <button onclick="window.print()" class="px-3 py-1.5 bg-slate-800 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5">
                            <i data-lucide="printer" class="w-3.5 h-3.5"></i> Imprimir Recibo
                        </button>
                    </div>

                    <!-- Printable Receipt Document Card -->
                    <div class="bg-white p-6 md:p-8 rounded-xl shadow-sm border border-slate-200 space-y-6 text-slate-800">
                        <!-- Receipt Header -->
                        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b pb-6 border-slate-200">
                            <div class="flex items-center gap-4">
                                <img src="${appState.building.logoUrl}" class="w-16 h-16 rounded-xl object-cover bg-slate-50 border" alt="Logo">
                                <div>
                                    <h2 class="text-lg font-bold text-slate-900">${appState.building.name}</h2>
                                    <p class="text-xs text-slate-500 font-mono">RIF: ${appState.building.rif}</p>
                                    <p class="text-[11px] text-slate-400 mt-0.5">${appState.building.address}</p>
                                </div>
                            </div>
                            <div class="text-right">
                                <span class="px-3 py-1 bg-blue-100 text-blue-800 text-xs font-extrabold rounded-full">AVISO DE COBRO</span>
                                <p class="text-xs font-bold text-slate-700 mt-2">PERÍODO: ${appState.selectedPeriod}</p>
                                <p class="text-[11px] text-slate-500">Tasa BCV: Bs. ${bill.rateBCV.toFixed(2)}</p>
                            </div>
                        </div>

                        <!-- Owner & Alicuota Info Box -->
                        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 p-4 bg-slate-50 rounded-xl text-xs">
                            <div>
                                <span class="text-slate-400">Apartamento:</span>
                                <p class="font-extrabold text-slate-800 text-sm">Apto ${aptId}</p>
                            </div>
                            <div>
                                <span class="text-slate-400">Propietario:</span>
                                <p class="font-bold text-slate-800">${bill.apt.owner}</p>
                            </div>
                            <div>
                                <span class="text-slate-400">Alícuota Aplicada:</span>
                                <p class="font-bold text-slate-800">${bill.apt.alicuota}%</p>
                            </div>
                            <div>
                                <span class="text-slate-400">Estado de Cuenta:</span>
                                <p class="font-bold ${balance.balanceUSD < -0.01 ? 'text-rose-600' : 'text-emerald-600'}">
                                    ${balance.balanceUSD < -0.01 ? 'Deuda Pendiente' : 'Al Día'}
                                </p>
                            </div>
                        </div>

                        <!-- Common Expenses Breakdown Table -->
                        <div>
                            <h3 class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">Desglose de Gastos Comunes del Edificio</h3>
                            <table class="w-full text-left text-xs border-collapse">
                                <thead>
                                    <tr class="bg-slate-100 text-slate-600 font-bold border-b">
                                        <th class="p-2">Descripción del Concepto</th>
                                        <th class="p-2 text-right">Monto Total USD</th>
                                        <th class="p-2 text-right">Monto Total Bs.</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-100">
                                    ${commonExpenses.length === 0 ? `
                                        <tr><td colspan="3" class="p-4 text-center text-slate-400">Sin gastos comunes este mes.</td></tr>
                                    ` : commonExpenses.map(e => `
                                        <tr>
                                            <td class="p-2 font-medium">${e.description}</td>
                                            <td class="p-2 text-right">${formatUSD(e.amountUSD)}</td>
                                            <td class="p-2 text-right text-slate-500">${formatBS(e.amountUSD * bill.rateBCV)}</td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>

                        <!-- Extra Quotas & Special Expenses -->
                        ${extraQuotas.length > 0 || uncommonExpenses.length > 0 ? `
                            <div>
                                <h3 class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">Cuotas Extraordinarias & Gastos Especiales Apto</h3>
                                <table class="w-full text-left text-xs border-collapse">
                                    <thead>
                                        <tr class="bg-slate-100 text-slate-600 font-bold border-b">
                                            <th class="p-2">Concepto</th>
                                            <th class="p-2">Tipo</th>
                                            <th class="p-2 text-right">Monto Apto USD</th>
                                        </tr>
                                    </thead>
                                    <tbody class="divide-y divide-slate-100">
                                        ${extraQuotas.map(eq => `
                                            <tr>
                                                <td class="p-2 font-medium">${eq.title}</td>
                                                <td class="p-2 text-blue-600 font-semibold">Cuota Extra (${bill.apt.alicuota}%)</td>
                                                <td class="p-2 text-right font-bold">${formatUSD((eq.totalAmountUSD * bill.apt.alicuota) / 100)}</td>
                                            </tr>
                                        `).join('')}
                                        ${uncommonExpenses.map(ue => `
                                            <tr>
                                                <td class="p-2 font-medium">${ue.description}</td>
                                                <td class="p-2 text-amber-600 font-semibold">Gasto No Común Apto</td>
                                                <td class="p-2 text-right font-bold">${formatUSD(ue.amountUSD)}</td>
                                            </tr>
                                        `).join('')}
                                    </tbody>
                                </table>
                            </div>
                        ` : ''}

                        <!-- Final Summary Calculations -->
                        <div class="border-t-2 border-slate-900 pt-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-slate-50 p-4 rounded-xl">
                            <div class="text-xs space-y-1 text-slate-600">
                                <p>• Gastos Comunes Alícuota (${bill.apt.alicuota}%): <strong>${formatUSD(bill.aptCommonUSD)}</strong></p>
                                <p>• Cuotas Extraordinarias Alícuota: <strong>${formatUSD(bill.aptExtraUSD)}</strong></p>
                                ${bill.aptUncommonUSD > 0 ? `<p>• Gastos No Comunes Directos: <strong>${formatUSD(bill.aptUncommonUSD)}</strong></p>` : ''}
                            </div>
                            <div class="text-right w-full sm:w-auto border-t sm:border-0 pt-2 sm:pt-0">
                                <p class="text-xs text-slate-500 font-bold uppercase">Total a Cancelar Mes</p>
                                <h3 class="text-2xl font-black text-blue-600">${formatUSD(bill.totalUSD)}</h3>
                                <p class="text-sm font-bold text-slate-700 mt-0.5">${formatBS(bill.totalBS)}</p>
                            </div>
                        </div>
                    </div>
                </div>
                `;
            } else if (currentOwnerTab === 'pay') {
                return `
                <div class="max-w-xl mx-auto bg-white p-6 rounded-xl shadow-sm border border-slate-200 space-y-5">
                    <h2 class="text-base font-bold text-slate-800 flex items-center gap-2">
                        <i data-lucide="send" class="w-5 h-5 text-blue-600"></i> Módulo Reportar Pago de Condominio
                    </h2>
                    <p class="text-xs text-slate-500">Ingrese los datos de su transferencia, pago móvil o reporte de divisas para su validación.</p>

                    <form onsubmit="handleOwnerPaymentSubmit(event)" class="space-y-4">
                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Período a Cancelar</label>
                                <input type="month" id="op-period" value="${appState.selectedPeriod}" class="w-full px-3 py-2 border rounded-lg text-xs bg-slate-50">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Moneda del Pago</label>
                                <select id="op-currency" onchange="updateOwnerPayConversion()" class="w-full px-3 py-2 border rounded-lg text-xs bg-slate-50">
                                    <option value="BS">Bolívares (Bs)</option>
                                    <option value="USD">Dólares Divisas (USD)</option>
                                </select>
                            </div>
                        </div>

                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Método de Pago</label>
                                <select id="op-method" class="w-full px-3 py-2 border rounded-lg text-xs bg-slate-50">
                                    <option value="Pago Móvil">Pago Móvil</option>
                                    <option value="Transferencia">Transferencia Bancaria</option>
                                    <option value="Efectivo USD">Efectivo USD</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Fecha de Transacción</label>
                                <input type="date" id="op-date" value="${new Date().toISOString().split('T')[0]}" required class="w-full px-3 py-2 border rounded-lg text-xs">
                            </div>
                        </div>

                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Monto Cancelado</label>
                                <input type="number" id="op-amount" step="0.01" required placeholder="0.00" oninput="updateOwnerPayConversion()" class="w-full px-3 py-2 border rounded-lg text-xs">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Nº Referencia / Confirmación</label>
                                <input type="text" id="op-ref" required placeholder="Ej: 99881122" class="w-full px-3 py-2 border rounded-lg text-xs font-mono">
                            </div>
                        </div>

                        <!-- BCV Auto Conversion Info Box -->
                        <div class="p-3 bg-blue-50 rounded-lg text-xs text-blue-800 flex justify-between items-center">
                            <span>Tasa Oficial del Día: <strong>Bs. ${appState.building.bcvRate.toFixed(2)}</strong></span>
                            <span id="op-conversion-preview" class="font-bold text-blue-700">Equivalente: $0.00</span>
                        </div>

                        <button type="submit" class="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-lg shadow-sm transition">
                            Enviar Reporte de Pago
                        </button>
                    </form>
                </div>
                `;
            } else if (currentOwnerTab === 'statement') {
                const myPayments = appState.payments.filter(p => p.aptId === aptId);

                return `
                <div class="space-y-6">
                    <!-- Balance Summary Cards -->
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <p class="text-xs text-slate-500 font-medium">Facturado Acumulado</p>
                            <h3 class="text-xl font-bold text-slate-800">${formatUSD(balance.billedUSD)}</h3>
                        </div>
                        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <p class="text-xs text-slate-500 font-medium">Pagado Aprobado</p>
                            <h3 class="text-xl font-bold text-emerald-600">${formatUSD(balance.paidUSD)}</h3>
                        </div>
                        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <p class="text-xs text-slate-500 font-medium">Saldo Actual</p>
                            <h3 class="text-xl font-bold ${balance.balanceUSD < -0.01 ? 'text-rose-600' : 'text-emerald-600'}">
                                ${balance.balanceUSD < -0.01 ? `Deuda: ${formatUSD(Math.abs(balance.balanceUSD))}` : `A Favor: ${formatUSD(balance.balanceUSD)}`}
                            </h3>
                        </div>
                    </div>

                    <!-- History of Payments -->
                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <h3 class="text-sm font-bold text-slate-800 mb-4">Historial de Pagos Reportados</h3>
                        <div class="overflow-x-auto custom-scrollbar">
                            <table class="w-full text-left text-xs">
                                <thead class="bg-slate-50 text-slate-500 uppercase">
                                    <tr>
                                        <th class="p-2.5">Fecha</th>
                                        <th class="p-2.5">Período</th>
                                        <th class="p-2.5">Método / Ref</th>
                                        <th class="p-2.5">Monto Reportado</th>
                                        <th class="p-2.5">Equiv. USD</th>
                                        <th class="p-2.5">Estado</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-100">
                                    ${myPayments.length === 0 ? `
                                        <tr><td colspan="6" class="p-6 text-center text-slate-400">No ha registrado pagos previamente.</td></tr>
                                    ` : myPayments.map(p => `
                                        <tr class="hover:bg-slate-50">
                                            <td class="p-2.5 font-medium">${p.date}</td>
                                            <td class="p-2.5 font-bold">${p.period}</td>
                                            <td class="p-2.5">
                                                <span class="font-medium">${p.method}</span>
                                                <div class="text-[10px] font-mono text-slate-400">Ref: ${p.reference}</div>
                                            </td>
                                            <td class="p-2.5 font-bold">${p.currency === 'BS' ? formatBS(p.amountBs) : formatUSD(p.amountUSD)}</td>
                                            <td class="p-2.5 font-semibold text-emerald-600">${formatUSD(p.amountUSD)}</td>
                                            <td class="p-2.5">
                                                ${p.status === 'APPROVED' ? 
                                                    `<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-700">Aprobado</span>` : 
                                                    p.status === 'PENDING' ?
                                                    `<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-700">En Revisión</span>` :
                                                    `<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-100 text-rose-700">Rechazado</span>`
                                                }
                                            </td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                `;
            }
        }

        function updateOwnerPayConversion() {
            const currency = document.getElementById('op-currency').value;
            const amount = parseFloat(document.getElementById('op-amount').value) || 0;
            const preview = document.getElementById('op-conversion-preview');

            if (currency === 'BS') {
                const usd = amount / appState.building.bcvRate;
                preview.innerText = `Equivalente: $${usd.toFixed(2)}`;
            } else {
                const bs = amount * appState.building.bcvRate;
                preview.innerText = `Equivalente: Bs. ${bs.toFixed(2)}`;
            }
        }

        function handleOwnerPaymentSubmit(e) {
            e.preventDefault();
            const period = document.getElementById('op-period').value;
            const currency = document.getElementById('op-currency').value;
            const method = document.getElementById('op-method').value;
            const date = document.getElementById('op-date').value;
            const rawAmount = parseFloat(document.getElementById('op-amount').value);
            const ref = document.getElementById('op-ref').value;

            let amountUSD = 0;
            let amountBs = 0;

            if (currency === 'BS') {
                amountBs = rawAmount;
                amountUSD = rawAmount / appState.building.bcvRate;
            } else {
                amountUSD = rawAmount;
                amountBs = rawAmount * appState.building.bcvRate;
            }

            const newPayment = {
                id: 'PAY-' + Date.now().toString().substr(-5),
                aptId: appState.currentUser.aptId,
                period: period,
                amountUSD: amountUSD,
                amountBs: amountBs,
                rateBCV: appState.building.bcvRate,
                currency: currency,
                method: method,
                reference: ref,
                date: date,
                status: 'PENDING',
                note: 'Reportado por Propietario'
            };

            appState.payments.push(newPayment);
            appState.saveState();
            showToast("Pago reportado con éxito. Queda en espera de revisión por la administración.");
            switchOwnerTab('statement');
        }

        // INITIAL RENDER CALL
        window.onload = function() {
            renderApp();
        };
    </script>
</body>
</html>
