import { Injectable } from '@angular/core'
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http'
import { ConfigApp } from '../services/config'
import { IHost } from '../date/IHost';

@Injectable({
    providedIn: 'root'
})
export class HostsService {
    constructor(private http: HttpClient, private config: ConfigApp) {

    }

    addHosts(host: IHost) {
        let headers = new HttpHeaders({
            'Content-Type': 'application/json'
        });
        let options = { headers: headers, body: host };

          
        return this.http.post(
            this.config.urlBackEnd + 'host', {"hostname": host.hostname, "password": host.password, "username": host.username}
        );
    }

    testConnection(host: IHost) {
        return this.http.post(
            this.config.urlBackEnd + 'task/test_connection', host
        )
    }

    getAllHosts() {
        return this.http.get(
            this.config.urlBackEnd + 'hosts'
        )
    }

    // get() {
    //     return this.http.get(this.config.urlBackEnd)
    // }
}