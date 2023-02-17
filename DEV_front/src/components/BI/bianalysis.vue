<template>
  <div v-if="error.length > 0" class="p-2 d-flex justify-content-center">
    <p style="color: crimson;">{{ error }}</p>
  </div>
  <div class="p-4 mb-4 d-flex" style="width: 100%; justify-content: space-between">
    <h3>Scroll down to see more analysis</h3>
    <a class="link text-primary" @click="download_slurm_log">Download SLURM log
    </a>
  </div>
  <!-- <div v-if="s_log_desc_loading" class="d-flex justify-content-center">
    <h5 class="text-warning">Loading...</h5>
  </div> -->

  <div class="d-flex flex-row justify-content-center" style="justify-content:center; align-items: center;">
    <div style="width:95%">
      <div class="d-flex flex-row" style="justify-content:space-between;">
        <div class="row p-4" style="width:50%">
          <div class="card m-auto">
            <div class="card-body">
              <div id="jobsnumovertime"></div>
              <p>Add analysis.</p>
            </div>
          </div>
        </div>
        <div class="row p-4" style="width:50%">
          <div class="card m-auto">
            <div class="card-body">
              <div id="jobsnumperaccount"></div>
              <p>Add analysis.</p>
            </div>
          </div>
        </div>
      </div>
      <div class="d-flex flex-row" style="justify-content:space-between;">
        <div class="row p-4" style="width:50%">
          <div class="card m-auto">
            <div class="card-body">
              <div id="jobsnumcpus"></div>
              <p>Add analysis.</p>
            </div>
          </div>
        </div>
        <div class="row p-4" style="width:50%">
          <div class="card m-auto">
            <div class="card-body">
              <div id="jobsStates"></div>
              <p>Add analysis.</p>
            </div>
          </div>
        </div>
      </div>
      <div class="d-flex flex-row" style="justify-content:space-between;">
        <div class="row p-4" style="width:50%">
          <div class="card m-auto">
            <div class="card-body">
              <div id="jobsovertimedurationcolored"></div>
              <p>Jobs took less than one hour to be completed are in <strong style="color: green;">green</strong>.<br>
                Jobs took less than one day to be completed are in <strong style="color: yellow;">yellow</strong>.<br>
                Jobs took less than one week to be completed are in <strong style="color: orange;">orange</strong>.<br>
                Jobs took less than one month to be completed are in <strong style="color: red;">red</strong>.<br></p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="w-100 p-3 d-flex justify-content-center">
    <ul class="w-50 list-group">
      <li class="list-group-item list-group-item-secondary d-flex justify-content-between align-items-center">
        Start Time
        <div v-if="s_log_desc_loading">
          <span class="badge badge-dark badge-pill p-2 text-warning">Loading...</span>
        </div>
        <h6><span class="badge badge-dark badge-pill p-2">{{ s_log_description['startTime'] }}</span></h6>
      </li>
      <li class="list-group-item list-group-item-secondary d-flex justify-content-between align-items-center">
        End Time
        <div v-if="s_log_desc_loading">
          <span class="badge badge-dark badge-pill p-2 text-warning">Loading...</span>
        </div>
        <span class="badge badge-dark badge-pill p-2">{{ s_log_description['endTime'] }}</span>
      </li>
      <li class="list-group-item list-group-item-secondary d-flex justify-content-between align-items-center">
        Number of events in the SLURM log
        <div v-if="s_log_desc_loading">
          <span class="badge badge-dark badge-pill p-2 text-warning">Loading...</span>
        </div>
        <span class="badge badge-dark badge-pill p-2">{{ s_log_description['eventsNumber'] }}</span>
      </li>
      <li class="list-group-item list-group-item-secondary d-flex justify-content-between align-items-center">
        Number of unique submitted jobs in the SLURM log
        <div v-if="s_log_desc_loading">
          <span class="badge badge-dark badge-pill p-2 text-warning">Loading...</span>
        </div>
        <span class="badge badge-dark badge-pill p-2">{{ s_log_description['jobNumber'] }}</span>
      </li>
      <li class="list-group-item list-group-item-secondary d-flex justify-content-between align-items-center">
        Number of unique accounts in the SLURM log
        <div v-if="s_log_desc_loading">
          <span class="badge badge-dark badge-pill p-2 text-warning">Loading...</span>
        </div>
        <span class="badge badge-dark badge-pill p-2">{{ s_log_description['accountNumber'] }}</span>
      </li>
      <li class="list-group-item list-group-item-secondary d-flex justify-content-between align-items-center">
        Percentage of accounts who submitted their jobs with explicit interdependencies
        <div v-if="s_log_desc_loading">
          <span class="badge badge-dark badge-pill p-2 text-warning">Loading...</span>
        </div>
        <span class="badge badge-dark badge-pill p-2">{{ s_log_description['SLURMaccountsPercentage'] }}</span>
      </li>
      <li class="list-group-item list-group-item-secondary d-flex justify-content-between align-items-center">
        Percentage of jobs were defined with explicit interdependencies
        <div v-if="s_log_desc_loading">
          <span class="badge badge-dark badge-pill p-2 text-warning">Loading...</span>
        </div>
        <span class="badge badge-dark badge-pill p-2">{{ s_log_description['SLURMjobssPercentage'] }}</span>
      </li>
      <li class="list-group-item list-group-item-secondary d-flex justify-content-between align-items-center">
        The average number of allocated CPUs
        <div v-if="s_log_desc_loading">
          <span class="badge badge-dark badge-pill p-2 text-warning">Loading...</span>
        </div>
        <span class="badge badge-dark badge-pill p-2">{{ s_log_description['CPUusageAvg'] }}</span>
      </li>
      <li class="list-group-item list-group-item-secondary d-flex justify-content-between align-items-center">
        The average number of allocated RAMs
        <div v-if="s_log_desc_loading">
          <span class="badge badge-dark badge-pill p-2 text-warning">Loading...</span>
        </div>
        <span class="badge badge-dark badge-pill p-2">{{ s_log_description['RAMusageAvg'] }}</span>
      </li>
    </ul>
  </div>
</template>
<script>
import { mapActions, mapWritableState } from "pinia";
import { slurmLogQueries } from "../../stores/APIs";
export default {
  name: "BIanalysis",
  methods: {
    sleep(time) {
      return new Promise((resolve) => setTimeout(resolve, time));
    },
    download(url) {
      window.location.href = url;
    },
    set_x_axis(x) {
      this.x_axis = x;
    },
    set_y_axis(y) {
      this.y_axis = y;
    },

    async download_slurm_log() {
      try {
        this.slurm_log_content = ""
        this.getData("");
        while (this.slurm_log_content.length == 0) {
          await this.sleep(1);
        }
        var a = document.createElement('a');
        a.href = this.slurm_log_content;
        let random_name = (Math.random() + 1).toString(36).substring(7);
        a.download = random_name + '.csv';
        document.body.appendChild(a);
        a.click();
      } catch (error) {
        console.log("error: ", error)
      }
    },
    ...mapActions(slurmLogQueries, ["getData"]),

    async get_scatter_plot() {
      try {
        this.error = ""
        this.distribution_model = ""
        this.scatter_model = ""
        this.getScatterPlotData({
          "x_axis": this.x_axis,
          "y_axis": this.y_axis
        });
      } catch (error) {
        console.log("error: ", error)
      }
    },
    ...mapActions(slurmLogQueries, ["getScatterPlotData"]),

    async get_job_distribution_plot() {
      try {
        this.error = ""
        this.scatter_model = ""
        this.distribution_model = ""
        this.getNumberOfSubmittedJobsOverTime()
        while (this.slurm_log_info.length == 0) {
          await this.sleep(1);
        }
        var slurm_log_info = JSON.parse(this.slurm_log_info)
        var plot_dimensions1 = {
          x: slurm_log_info["TIMESTAMP"],
          y: slurm_log_info["JOBCOUNT"],
          type: 'bar'
        };
        var plot_data = [plot_dimensions1];
        var layout = {
          title: 'Number of Submitted Jobs over Time',
          showlegend: false,
          fixedrange: false,
          xaxis: {
            title: "time",
            // type: 'linear',
            // showgrid: true,
            // autorange: true,
          },
          yaxis: {
            title: "submited jobs count",
            type: 'linear',
          },
        };
        Plotly.plot('jobsnumovertime', plot_data, layout, { scrollZoom: true });

        while (this.CPUS_JOBCOUNT.length == 0) {
          await this.sleep(1);
        }
        var CPUS_JOBCOUNT = JSON.parse(this.CPUS_JOBCOUNT)
        var plot_dimensions2 = {
          x: CPUS_JOBCOUNT["CPUS_JOBCOUNT"],
          y: CPUS_JOBCOUNT["CPUS"],
          type: 'bar',
          orientation: 'h'
        };
        var plot_data2 = [plot_dimensions2];
        var layout2 = {
          title: '#Jobs and Requested CPUs',
          showlegend: false,
          fixedrange: false,
          xaxis: {
            title: "number of jobs",
            type: 'linear',
          },
          yaxis: {
            title: "number of requested CPUs",
          },
        };
        Plotly.plot('jobsnumcpus', plot_data2, layout2, { scrollZoom: true });


        while (this.R_PD_TIME.length == 0) {
          await this.sleep(1);
        }
        var R_PD_TIME = JSON.parse(this.R_PD_TIME)
        var plot_dimensions3 = {
          x: R_PD_TIME["times"],
          y: R_PD_TIME["Rnums"],
          name: '#running',
          type: 'bar',
          orientation: 'v'
        };
        var plot_dimensions4 = {
          x: R_PD_TIME["times"],
          y: R_PD_TIME["PDnums"],
          name: '#pending',
          type: 'bar',
          orientation: 'v'
        };
        var plot_data3 = [plot_dimensions3, plot_dimensions4];
        var layout3 = {
          title: '#of Running and Pending Jobs over Time',
          showlegend: true,
          fixedrange: false,
          xaxis: {
            title: "time",
          },
          yaxis: {
            title: "number of running & pending jobs ",
            type: 'linear',
          },
        };
        Plotly.plot('jobsStates', plot_data3, layout3, { scrollZoom: true });


      } catch (error) {
        console.log("error: ", error)
      }
    },
    ...mapActions(slurmLogQueries, ["getNumberOfSubmittedJobsOverTime"]),

    async get_job_distribution_per_account_plot() {
      try {
        this.error = ""
        this.scatter_model = ""
        this.distribution_model = ""
        this.getNumberOfSubmittedJobsPerAccount()
        while (this.jobs_per_account.length == 0) {
          await this.sleep(1);
        }
        var jobs_per_account = JSON.parse(this.jobs_per_account)

        var plot_dimensions1 = {
          x: jobs_per_account["JOBCOUNT"],
          y: jobs_per_account["ACCOUNTS"],
          type: 'bar',
          orientation: 'h'
        };
        var plot_data = [plot_dimensions1];
        var layout = {
          title: 'Number of Submitted Jobs Per Account',
          showlegend: false,
          fixedrange: false,
          xaxis: {
            title: "number of submited jobs",
            type: 'linear',
          }
        };

        Plotly.plot('jobsnumperaccount', plot_data, layout, { scrollZoom: true });


      } catch (error) {
        console.log("error: ", error)
      }
    },
    ...mapActions(slurmLogQueries, ["getNumberOfSubmittedJobsPerAccount"]),

    async get_dotted_chart_jobid_duration_label() {
      try {
        this.error = ""
        this.scatter_model = ""
        this.distribution_model = ""
        this.getDottedJobidDurationLabel()
        while (this.time_jobs_state.length == 0) {
          await this.sleep(1);
        }
        var time_jobs_state = JSON.parse(this.time_jobs_state)
        var trace1 = {
          x: time_jobs_state['START'],
          y: time_jobs_state['JOBID_view'],
          mode: 'markers',
          type: 'scatter',
          name: time_jobs_state['DURATION_LABEL'],
          marker: {
            color: time_jobs_state['DURATION_LABEL']
          }
        };

        var data = [trace1];
        var layout = {
          title: 'JobID over Submitted time, colored by duration',
          showlegend: false,
          fixedrange: false,
          xaxis: {
            title: "time",
          }
        };
        Plotly.plot('jobsovertimedurationcolored', data, layout, { scrollZoom: true });

      } catch (error) {
        console.log("error: ", error)
      }
    },
    ...mapActions(slurmLogQueries, ["getDottedJobidDurationLabel"]),

    async get_slurm_log_description() {
      try {
        this.slurmLogDescription()
      } catch (error) {
        console.log("error: ", error)
      }
    },
    ...mapActions(slurmLogQueries, ["slurmLogDescription"]),

  },
  computed: {
    ...mapWritableState(slurmLogQueries, [
      "slurm_log_content",
      "scatter_model",
      "error",
      "distribution_model",
      "slurm_log_info",
      "jobs_per_account",
      "time_jobs_state",
      'CPUS_JOBCOUNT',
      "R_PD_TIME",
      "s_log_description",
      "s_log_desc_loading",
      "distribution_loading"
    ]),
  },
  beforeMount() {
    this.error = ""
  },
  mounted() {
    this.get_job_distribution_plot();
    this.get_job_distribution_per_account_plot();
    this.get_dotted_chart_jobid_duration_label();
    this.get_slurm_log_description()
  },
};
</script>