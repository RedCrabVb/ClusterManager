import { Injectable } from '@angular/core'
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http'
import { ConfigApp } from '../services/config'
import { Utils } from './utils';

@Injectable({
    providedIn: 'root'
})
export class ProcStatusService {
    constructor(private http: HttpClient, private config: ConfigApp) {

    }

    getAuthHeader() {
        let headers = new HttpHeaders({
            'Authorization': `${Utils.getCookie('token_type')} ${Utils.getCookie('access_token')}`
        });

        return {headers: headers};
    }

    getTaskStatuses() {
        return this.http.get(
            this.config.urlBackEnd + 'task/statuses', this.getAuthHeader()
        );
    }

    getTaskStatus(proc_id: number) {
        return this.http.get(
            this.config.urlBackEnd + 'task/status?proc_id=' + proc_id, this.getAuthHeader()
        );
    }
}