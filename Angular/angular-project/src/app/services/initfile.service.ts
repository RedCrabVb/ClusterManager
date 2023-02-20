import { Injectable } from '@angular/core'
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http'
import { ConfigApp } from '../services/config'

@Injectable({
    providedIn: 'root'
})
export class InitFileService {
    constructor(private http: HttpClient, private config: ConfigApp) {

    }

    // todo: limit version
    uploadFile(namefile: string, data: string, name: string) {
        let headers = new HttpHeaders({
            'Content-Type': 'application/json'
        });
        let options = { headers: headers, body: { namefile, data, name } };


        return this.http.post(
            this.config.urlBackEnd + 'upload/initfile', { namefile, data, name }
        );
    }

    getAllInitfiles() {
        return this.http.get(
            this.config.urlBackEnd + 'initfile'
        )
    }

    get() {
        return this.http.get(this.config.urlBackEnd)
    }
}