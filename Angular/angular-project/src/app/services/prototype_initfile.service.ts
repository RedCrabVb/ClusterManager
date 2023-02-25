import { Injectable } from '@angular/core'
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http'
import { ConfigApp } from '../services/config'
import { Utils } from './utils';

@Injectable({
    providedIn: 'root'
})
export class PrototypeInitFileService {
    constructor(private http: HttpClient, private config: ConfigApp) {

    }

    getAuthHeader() {
        let headers = new HttpHeaders({
            'Authorization': `${Utils.getCookie('token_type')} ${Utils.getCookie('access_token')}`
        });

        return {headers: headers};
    }

    openFile(namefile: string, path: string, name: string, version: string) {
        return this.http.get(this.config.urlBackEnd + 
            `initfile/prototype/load?name=${name}&version=${version}&path=${path}&namefile=${namefile}`, this.getAuthHeader())
    }

    viewDir(name: string, version: string, path: string) {
        return this.http.get(this.config.urlBackEnd + 
            `initfile/prototype?name=${name}&version=${version}&path=${path}`, this.getAuthHeader())
    }

    get() {
        return this.http.get(this.config.urlBackEnd, this.getAuthHeader())
    }
}