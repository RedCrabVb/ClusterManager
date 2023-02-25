import { Injectable } from '@angular/core'
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http'
import { ConfigApp } from '../services/config'
import { IHost } from '../date/IHost';
import { Utils } from './utils';

@Injectable({
    providedIn: 'root'
})
export class HostsService {
    constructor(private http: HttpClient, private config: ConfigApp) {

    }

    deleteHost(host: IHost) {
        let headers = new HttpHeaders({
            'Authorization': `${Utils.getCookie('token_type')} ${Utils.getCookie('access_token')}`
        });

        return this.http.post(
            this.config.urlBackEnd + 'host/delete', { "hostname": host.hostname, "password": host.password, "username": host.username }, { headers }
        );
    }

    addHosts(host: IHost) {
        let headers = new HttpHeaders({
            'Authorization': `${Utils.getCookie('token_type')} ${Utils.getCookie('access_token')}`
        });

        return this.http.post(
            this.config.urlBackEnd + 'host', host, { headers }
        );
    }

    testConnection(host: IHost) {
        let headers = new HttpHeaders({
            'Authorization': `${Utils.getCookie('token_type')} ${Utils.getCookie('access_token')}`
        });

        return this.http.post(
            this.config.urlBackEnd + 'task/test_connection', host, { headers }
        )
    }

    getAllHosts() {
        let headers = new HttpHeaders({
            'Authorization': `${Utils.getCookie('token_type')} ${Utils.getCookie('access_token')}`
        });

        return this.http.get(
            this.config.urlBackEnd + 'hosts', { headers }
        )
    }

}