var app = new Vue({
    el: '#vue-app',
    data: {
        progressWidth: '0%',
        modelSpec: LLM_SPECS[0],
        budget: 50,
        showParams: false,
        showResetConfirmation: false,
        enableChartDiagram: true,
        enableLogging: false,
        enableConcurrency: false,
        optimize: false,
        enableMultiStepAttack: false,
        scanResults: [],
        mainTable: [],
        integrationVerified: false,
        scanRunning: false,
        errorMsg: '',
        maskMode: false,
        okMsg: '',
        reportImageUrl: '',
        selectedConfig: 0,
        showModules: false,
        showLogs: false,
        showConsentModal: true,
        statusDotClass: 'bg-gray-500', // Default status dot class
        statusText: 'Verified', // Default status text
        statusClass: 'bg-green-500 text-dark-bg', // Default status class
        showLLMSpec: true, // Default to showing the LLM Spec Input
        logs: [], // This will store all the logs
        maxDisplayedLogs: 50, // Maximum number of logs to display
        configs: [
            { name: 'Custom API', prompts: 40000, customInstructions: 'Requires api spec' },
            { name: 'Open AI', prompts: 24000 },
            { name: 'Replicate', prompts: 40000 },
            { name: 'Groq', prompts: 40000 },
            { name: 'Together.ai', prompts: 40000 },
        ],
        dataConfig: [],
    },
    created() {
        // Check if consent is already given in local storage
        const consentGiven = localStorage.getItem('consentGiven');
        if (consentGiven === 'true') {
            this.showConsentModal = false; // Don't show the modal if consent was given
        }
    },
    mounted: function () {
        console.log('Vue app mounted');
        this.adjustHeight({ target: document.getElementById('llm-spec') });
        // this.startScan();
        this.loadConfigs();

    },
    computed: {
        selectedDS: function () {
            return this.dataConfig.filter(p => p.selected).length;
        },
        displayedLogs() {
            return this.logs.slice(-this.maxDisplayedLogs).reverse();
        }
    },
    methods: {
        acceptConsent() {
            this.showConsentModal = false; // Close the modal
            localStorage.setItem('consentGiven', 'true'); // Save consent to local storage
        },

        saveStateToLocalStorage() {
            const state = {
                modelSpec: this.modelSpec,
                budget: this.budget,
                dataConfig: this.dataConfig,
                optimize: this.optimize,
                enableChartDiagram: this.enableChartDiagram,
                enableMultiStepAttack: this.enableMultiStepAttack,
            };
            localStorage.setItem('appState', JSON.stringify(state));
        },
        loadStateFromLocalStorage() {
            const savedState = localStorage.getItem('appState');
            console.log('Loading state from local storage:', savedState);
            if (savedState) {
                const state = JSON.parse(savedState);
                this.modelSpec = state.modelSpec;
                this.budget = state.budget;
                this.dataConfig = state.dataConfig;
                this.optimize = state.optimize;
                this.enableChartDiagram = state.enableChartDiagram;
                this.enableMultiStepAttack = state.enableMultiStepAttack;
            }
        },
        resetState() {
            localStorage.removeItem('appState');
            this.modelSpec = LLM_SPECS[0];
            this.budget = 50;
            this.dataConfig.forEach(config => config.selected = false);
            this.optimize = false;
            this.enableChartDiagram = true;
            this.okMsg = '';
            this.errorMsg = '';
            this.integrationVerified = false;
            this.showResetConfirmation = false;
            this.enableMultiStepAttack = false;
        },
        confirmResetState() {
            this.showResetConfirmation = true;
        },

        declineConsent() {
            this.showConsentModal = false; // Close the modal
            localStorage.setItem('consentGiven', 'false'); // Save decline to local storage
            window.location.href = 'https://www.google.com'; // Redirect to Google
        },
        updateStatusDot(ok) {
            if (ok) {
                this.statusDotClass = 'bg-green-500'; // Green when expanded
            } else if (!ok) {
                this.statusDotClass = 'bg-orange-500'; // Orange if collapsed with content
            } else {
                this.statusDotClass = 'bg-gray-500'; // Gray if collapsed without content
            }
        },
        toggleLLMSpec() {
            this.showLLMSpec = !this.showLLMSpec;
        },
        adjustHeight(event) {
            event.target.style.height = 'auto';
            event.target.style.height = event.target.scrollHeight + 'px';
        },
        downloadFailures() {
            window.open('/failures', '_blank');
        },
        hide() {
            this.maskMode = !this.maskMode;
        },
        verifyIntegration: async function () {
            let payload = {
                spec: this.modelSpec,
            };
            const response = await fetch(`${URL}/verify`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });
            console.log(response);
            let txt = await response.text();
            if (!response.ok) {
                this.updateStatusDot(false);
                this.errorMsg = 'Integration verification failed:' + txt;
            } else {
                this.errorMsg = '';
                this.updateStatusDot(true);
                this.okMsg = 'Integration verified';
                this.integrationVerified = true;
                // console.log('Integration verified', this.integrationVerified);
                // this.$forceUpdate();

            }
            this.saveStateToLocalStorage();
        },
        loadConfigs: async function () {
            const response = await fetch(`${URL}/v1/data-config`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            console.log(response);
            this.dataConfig = await response.json();
            this.loadStateFromLocalStorage();
        },
        selectConfig(index) {
            this.selectedConfig = index;
            this.modelSpec = LLM_SPECS[index];
            this.adjustHeight({ target: document.getElementById('llm-spec') });
            // this.adjustHeight({ target: document.getElementById('llm-spec') });
            this.errorMsg = '';
            this.okMsg = '';
            this.integrationVerified = false;
        },
        toggleModules() {
            this.showModules = !this.showModules;
        },
        toggleLogs() {
            this.showLogs = !this.showLogs;
        },
        addLog(message, level = 'INFO') {
            const timestamp = new Date().toISOString();
            this.logs.push({ timestamp, message, level });
        },
        downloadLogs() {
            const logText = this.logs.map(log => `${log.timestamp} [${log.level}] ${log.message}`).join('\n');
            const blob = new Blob([logText], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'vulnerability_scan_logs.txt';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        },
        addPackage(index) {

            package = this.dataConfig[index];
            package.selected = !package.selected;

        },
        getFailureRateScore(failureRate) {
            // Convert failureRate to a strength percentage
            const strengthRate = 100 - failureRate;

            if (strengthRate >= 90) return 'A';
            else if (strengthRate >= 80) return 'B';
            else if (strengthRate >= 70) return 'C';
            else if (strengthRate >= 60) return 'D';
            else return 'E'; // For strengthRate less than 60
        },
        getFailureRateColor(failureRate) {
            // We're now working with the strength percentage, so no need to invert
            const strengthRate = 100 - failureRate;

            if (strengthRate >= 95) return 'text-green-400';
            else if (strengthRate >= 85) return 'text-green-400';
            else if (strengthRate >= 75) return 'text-green-500';
            else if (strengthRate >= 65) return 'text-yellow-400';
            else if (strengthRate >= 55) return 'text-yellow-500';
            else if (strengthRate >= 45) return 'text-orange-400';
            else if (strengthRate >= 35) return 'text-orange-500';
            else if (strengthRate >= 25) return 'text-dark-accent-red';
            else if (strengthRate >= 15) return 'text-red-400';
            else if (strengthRate > 0) return 'text-red-500';
            else return 'text-gray-100'; // This can be the default for strengthRate of 0 or less
        },
        toggleParams() {
            this.showParams = !this.showParams;
        },
        adjustHeight(event) {
            const element = event.target;
            // Reset height to ensure accurate measurement
            element.style.height = 'auto';
            // Adjust height based on scrollHeight
            element.style.height = `${element.scrollHeight + 100}px`;
        },
        newEvent: function (event) {

            if (event.status) {
                this.okMsg = `${event.module}`;
                return
            }
            console.log('New event');
            //  { "module": "Module 49", "tokens": 480, "cost": 4.800000000000001, "progress": 9.8 }
            let progress = event.progress;
            progress = progress % 100;
            this.progressWidth = `${progress}%`;
            this.addLog(`${JSON.stringify(event)}`, 'INFO');
            if (this.mainTable.length < 1) {
                this.mainTable.push(event);
                event.last = true;

                return
            }
            let last = this.mainTable[this.mainTable.length - 1];
            if (last.module === event.module) {
                last.tokens = event.tokens;
                last.cost = event.cost;
                last.progress = event.progress;
                last.failureRate = event.failureRate;
            } else {
                last.last = false;
                this.mainTable.push(event);
                event.last = true;
                this.newRow()
            }
            this.okMsg = `New event: ${event.module}: ${event.progress}%`;

        },
        newRow: async function () {
            if (!this.enableChartDiagram) {
                return
            }
            console.log('New row');
            let payload = {
                table: this.mainTable,
            };
            const response = await fetch(`${URL}/plot.jpeg`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });
            // Convert image response to a data URL for the <img> src
            const blob = await response.blob();
            const reader = new FileReader();
            reader.readAsDataURL(blob);
            reader.onloadend = () => {
                this.reportImageUrl = reader.result;
            };
        },
        selectAllPackages() {
            const allSelected = this.dataConfig.every(package => package.selected);

            // If all are selected, deselect all. Otherwise, select all.
            this.dataConfig.forEach(package => {
                package.selected = !allSelected;
            });

            this.updateSelectedDS();
        },

        deselectAllPackages() {
            this.dataConfig.forEach(package => {
                package.selected = false;
            });
            this.updateSelectedDS();
        },

        updateSelectedDS() {
            this.selectedDS = this.dataConfig.filter(package => package.selected).length;
        },
        updateBudgetFromSlider(event) {
            this.budget = parseInt(event.target.value);
        },
        updateBudgetFromInput(event) {
            let value = parseInt(event.target.value);
            if (isNaN(value) || value < 1) {
                value = 1;
            } else if (value > 100) {
                value = 100;
            }
            this.budget = value;
        },
        stopScan: async function () {
            this.scanRunning = false;
            const response = await fetch(`${URL}/stop`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
        },
        startScan: async function () {
            this.showLLMSpec = false;
            let payload = {
                maxBudget: this.budget,
                llmSpec: this.modelSpec,
                datasets: this.dataConfig,
                optimize: this.optimize,
                enableMultiStepAttack: this.enableMultiStepAttack,
            };
            const response = await fetch(`${URL}/scan`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });
            this.okMsg = 'Scan started';
            this.mainTable = [];
            this.scanRunning = true;
            const reader = response.body.getReader();
            let receivedLength = 0; // received that many bytes at the moment
            let chunks = []; // array of received binary chunks (comprises the body)
            while (true) {
                const { done, value } = await reader.read();

                if (done) {
                    break;
                }

                chunks.push(value);
                receivedLength += value.length;

                const chunkAsString = new TextDecoder("utf-8").decode(value);
                const chunkAsLines = chunkAsString.split('\n').filter(line => line.trim());

                self = this;
                chunkAsLines.forEach(line => {
                    try {
                        const result = JSON.parse(line);
                        self.scanResults.push(result);
                        self.newEvent(result);
                    } catch (e) {
                        console.error('Error parsing chunk:', e);
                    }
                });
            }
            this.saveStateToLocalStorage();

        }
    }
});
