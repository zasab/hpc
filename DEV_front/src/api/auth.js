import http from "./helper/http";


export default new class AuthService {
    login(login) {
        return http.post("/start_logging", login);
    }

    get_model(get_model) {
        return http.post("/discover_model", get_model);
    }

    restart_logging(restart_logging) {
        return http.post("/restart_logging", restart_logging);
    }

    get_slurm_log(get_slurm_log) {
        return http.post("/get_slurm_log", get_slurm_log)
    }

    get_normal_event_log(get_normal_event_log) {
        return http.post("/get_normal_event_log", get_normal_event_log)
    }

    get_ocel_log(get_ocel_log) {
        return http.post("/get_ocel_log", get_ocel_log)
    }

    get_slurm_log_dotted_chart(get_slurm_log_dotted_chart) {
        return http.post("/get_slurm_log_dotted_chart", get_slurm_log_dotted_chart)
    }

    job_distribution_over_time(job_distribution_over_time) {
        return http.post("/job_distribution_over_time", job_distribution_over_time)
    }

    job_distribution_per_account(job_distribution_per_account) {
        return http.post("/job_distribution_per_account", job_distribution_per_account)
    }

    dottet_chart_jobid_duration_label(dottet_chart_jobid_duration_label) {
        return http.post("/dottet_chart_jobid_duration_label", dottet_chart_jobid_duration_label)
    }

    get_slurm_log_column_values(get_slurm_log_column_values) {
        return http.post("/get_slurm_log_column_values", get_slurm_log_column_values)
    }

    slurm_log_description(slurm_log_description) {
        return http.post("/slurm_log_description", slurm_log_description)
    }
}

