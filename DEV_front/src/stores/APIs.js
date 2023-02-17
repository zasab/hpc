import { defineStore } from 'pinia'
import authService from "@/api/auth.js";


export const startLoggingQuery = defineStore({
  id: 'table',
  state: () => ({
    table: {},
    totalCount: 20,
    username: "de467102",
    password: "",
    serverhost: "login18-1.hpc.itc.rwth-aachen.de",
    page: 1,
    limit: 3,
    error: "",
    accounts: 0,
    job_id_numbers: 0,
    min_time: "",
    max_time: ""
  }),
  getters: {
    headers: (state) => state.table.header,
    body: (state) => state.table.content,
  },


  actions: {
    async getData() {
      try {
        this.error = "";
        const res = await authService.login({
          username: this.username,
          password: this.password,
          serverhost: this.serverhost,
        });
        this.accounts = res.data.accounts,
          this.job_id_numbers = res.data.job_id_numbers,
          this.min_time = res.data.min_time,
          this.max_time = res.data.max_time
      } catch (error) {
        if (error.response) {
          this.error = error.response.data.error
        }
        else {
          this.error = error.message;
        }
      }
    },
    async restart_logging() {
      try {
        this.error = "";
        const res = await authService.restart_logging({
          username: this.username,
          password: this.password,
          serverhost: this.serverhost,
        });
        this.accounts = res.data.accounts,
          this.job_id_numbers = res.data.job_id_numbers,
          this.min_time = res.data.min_time,
          this.max_time = res.data.max_time
      } catch (error) {
        if (error.response) {
          this.error = error.response.data.error
        }
        else {
          this.error = error.message;
        }
      }
    }
  }
})

export const discoverModelQuery = defineStore({
  id: 'model',
  state: () => ({
    account: "default",
    cc_model: "",
    cc_fitness: "",
    ag_model: "",
    ag_fitness: "",
    discovery_error: "",
    loading: false
  }),

  actions: {
    async getModel() {
      try {
        this.discovery_error = ""
        this.loading = true
        const res = await authService.get_model({ account: this.account });
        if (res.data.hasOwnProperty('cc_model')) {
          this.cc_model = "data:image/jpeg;base64," + res.data.cc_model;
          this.cc_fitness = res.data.cc_fitness;
          this.ag_model = "data:image/jpeg;base64," + res.data.ag_model;
          this.ag_fitness = res.data.ag_fitness;
          this.loading = false;
        }
      } catch (error) {
        if (error.response) {
          this.discovery_error = error.response.data.error
        }
        else {
          this.discovery_error = error.message;
        }
        this.cc_model = "";
        this.cc_fitness = "";
        this.ag_model = "";
        this.ag_fitness = "";
        this.loading = false
      }
    },
  }
})

export const slurmLogQueries = defineStore({
  id: 'slurm-log',
  state: () => ({
    slurm_log_content: "",
    normal_log_content: "",
    ocel_log_content: "",
    scatter_model: "",
    distribution_model: "",
    slurm_log_info: "",
    CPUS_JOBCOUNT: "",
    R_PD_TIME: "",
    jobs_per_account: "",
    time_jobs_state: "",
    unique_accounts: "",
    s_log_description: "",
    s_log_desc_loading: false,
    x_axis: "",
    y_axis: "",
    distribution_loading: false,
    get_log_loading: false,
    error: ""
  }),

  actions: {
    async getData() {
      try {
        this.error = "";
        const res = await authService.get_slurm_log({
          slurm_log_content: this.slurm_log_content
        });
        const blob = new Blob([res.data], { type: 'text/csv' })
        this.slurm_log_content = URL.createObjectURL(blob);
      } catch (error) {
        if (error.response) {
          this.error = error.response.data.error
        }
        else {
          this.error = error.message;
        }
        this.slurm_log_content = "";

      }
    },

    async getNormalEventLog() {
      try {
        this.error = "";
        this.get_log_loading = true;
        const res = await authService.get_normal_event_log({
          normal_log_content: this.normal_log_content
        });
        const blob = new Blob([res.data], { type: 'text/csv' })
        this.normal_log_content = URL.createObjectURL(blob);
        this.get_log_loading = false;
      } catch (error) {
        if (error.response) {
          this.error = error.response.data.error
        }
        else {
          this.error = error.message;
        }
        this.normal_log_content = "";
        this.get_log_loading = false;

      }
    },

    async getOCELLog() {
      try {
        this.error = "";
        const res = await authService.get_ocel_log({
          ocel_log_content: ""
        });

        var jsonse = JSON.stringify(res.data);
        const blob = new Blob([jsonse], { type: 'application/json' })
        this.ocel_log_content = URL.createObjectURL(blob);
      } catch (error) {
        if (error.response) {
          this.error = error.response.data.error
        }
        else {
          this.error = error.message;
        }
        this.ocel_log_content = "";
      }
    },

    async getScatterPlotData(axis_data) {
      try {
        this.scatter_loading = true
        this.error = ""
        const res = await authService.get_slurm_log_dotted_chart({
          x_axis: axis_data.x_axis,
          y_axis: axis_data.y_axis
        });
        if (res.data.hasOwnProperty('scatter_model')) {
          this.scatter_model = "data:image/jpeg;base64," + res.data.scatter_model;
          this.scatter_loading = false
        }
      } catch (error) {
        if (error.response) {
          this.error = error.response.data.error
        }
        else {
          this.error = error.message;
        }
        this.scatter_model = "";
        this.scatter_loading = false

      }
    },

    async getNumberOfSubmittedJobsOverTime() {
      try {
        this.error = ""
        const res = await authService.job_distribution_over_time({ "nothing": "" });
        if (res.data.hasOwnProperty('slurm_log_info')) {
          this.distribution_model = ""
          this.slurm_log_info = res.data.slurm_log_info;
        }
        if (res.data.hasOwnProperty('CPUS_JOBCOUNT')) {
          this.CPUS_JOBCOUNT = res.data.CPUS_JOBCOUNT;
        }
        if (res.data.hasOwnProperty('R_PD_TIME')) {
          this.R_PD_TIME = res.data.R_PD_TIME;
        }
      } catch (error) {
        if (error.response) {
          this.error = error.response.data.error
        }
        else {
          this.error = error.message;
        }
        this.distribution_model = "";
        this.slurm_log_info = "";
        this.CPUS_JOBCOUNT = "";
        this.R_PD_TIME = "";

      }
    },

    async getNumberOfSubmittedJobsPerAccount() {
      try {
        this.error = ""
        const res = await authService.job_distribution_per_account({ "nothing": "" });
        if (res.data.hasOwnProperty('jobs_per_account')) {
          this.distribution_model = ""
          this.jobs_per_account = res.data.jobs_per_account;
        }
      } catch (error) {
        if (error.response) {
          this.error = error.response.data.error
        }
        else {
          this.error = error.message;
        }
        this.distribution_model = "";
        this.jobs_per_account = "";

      }
    },

    async getDottedJobidDurationLabel() {
      try {
        this.distribution_loading = true
        this.error = ""
        const res = await authService.dottet_chart_jobid_duration_label({ "nothing": "" });
        if (res.data.hasOwnProperty('time_jobs_state')) {
          this.distribution_model = ""
          this.time_jobs_state = res.data.time_jobs_state;
          this.distribution_loading = false
        }
      } catch (error) {
        if (error.response) {
          this.error = error.response.data.error
        }
        else {
          this.error = error.message;
        }
        this.distribution_model = "";
        this.time_jobs_state = "";
        this.distribution_loading = false

      }
    },

    async getSlurmLogColumnValues() {
      try {
        this.error = ""
        const res = await authService.get_slurm_log_column_values({ "nothing": "" });
        if (res.data.hasOwnProperty('slurm_column_values')) {
          while (res.data.slurm_column_values.length == 0) {
            await this.sleep(1);
          }
          var slurmcolumnvalues = JSON.parse(res.data.slurm_column_values)
          this.unique_accounts = slurmcolumnvalues['unique_accounts']
        }
      } catch (error) {
        if (error.response) {
          this.error = error.response.data.error
        }
        else {
          this.error = error.message;
        }
      }
    },

    async slurmLogDescription() {
      try {
        this.error = ""
        this.s_log_desc_loading = true
        this.s_log_description = ""
        const res = await authService.slurm_log_description({ "nothing": "" });
        if (res.data.hasOwnProperty('s_log_description')) {
          while (res.data.s_log_description.length == 0) {
            await this.sleep(1);
          }
          this.s_log_description = res.data.s_log_description
          this.s_log_desc_loading = false
        }
      } catch (error) {
        if (error.response) {
          this.error = error.response.data.error
          this.s_log_desc_loading = false
        }
        else {
          this.error = error.message;
          this.s_log_desc_loading = false
        }
      }
    }

  }
})