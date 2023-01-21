import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { ConfigApp } from "./config";

@Injectable({
    providedIn: 'root'
})
export class ClusterService {
    constructor(private http: HttpClient, private config: ConfigApp) {

    }

    getAllHosts() {
        return this.http.get(
            this.config.urlBackEnd + 'cluster'
        )
    }
}