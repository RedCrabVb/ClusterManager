import { Injectable } from '@angular/core'
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http'
import { ConfigApp } from '../services/config'
import { Utils } from './utils';

@Injectable({
    providedIn: 'root'
})
export class InitFileService {
    constructor(private http: HttpClient, private config: ConfigApp) {

    }

    acceptLicense(name: string, version: string) {
        let headers = new HttpHeaders({
            'Authorization': `${Utils.getCookie('token_type')} ${Utils.getCookie('access_token')}`
        });

        return this.http.post(
            this.config.urlBackEnd + 'initfile/accept', { name, version }, { headers }
        );
    } 

    // todo: limit version
    uploadFile(namefile: string, data: string, name: string) {
        let headers = new HttpHeaders({
            'Authorization': `${Utils.getCookie('token_type')} ${Utils.getCookie('access_token')}`
        });

        return this.http.post(
            this.config.urlBackEnd + 'upload/initfile', { namefile, data, name }, { headers }
        );
    }

    deleteFile(name: string, version: string) {
        let headers = new HttpHeaders({
            'Authorization': `${Utils.getCookie('token_type')} ${Utils.getCookie('access_token')}`
        });

        return this.http.post(
            this.config.urlBackEnd + 'initfile/delete', { name, version }, { headers }
        );
    }

    getAllInitfiles() {
        let headers = new HttpHeaders({
            'Authorization': `${Utils.getCookie('token_type')} ${Utils.getCookie('access_token')}`
        });

        return this.http.get(
            this.config.urlBackEnd + 'initfile', { headers }
        )
    }

    get() {
        let headers = new HttpHeaders({
            'Authorization': `${Utils.getCookie('token_type')} ${Utils.getCookie('access_token')}`
        });

        return this.http.get(this.config.urlBackEnd, { headers })
    }
}