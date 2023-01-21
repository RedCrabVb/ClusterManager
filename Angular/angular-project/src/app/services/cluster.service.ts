import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { ConfigApp } from "./config";
import { ICluster } from "../date/ICluster";

@Injectable({
    providedIn: 'root'
})
export class ClusterService {
    constructor(private http: HttpClient, private config: ConfigApp) {

    }

    getAllCluster() {
        return this.http.get(
            this.config.urlBackEnd + 'cluster'
        )
    }

    createCluster(clusetr: ICluster) {
        return this.http.post(
            this.config.urlBackEnd + 'cluster', { name: clusetr.name, description: clusetr.description, initfile_name: clusetr.initfile }
        )
    }
}