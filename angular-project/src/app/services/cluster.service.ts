import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { ConfigApp } from "./config";
import { ICluster } from "../date/ICluster";
import { IHost } from "../date/IHost";
import { Utils } from "./utils";

@Injectable({
    providedIn: 'root'
})
export class ClusterService {
    constructor(private http: HttpClient, private config: ConfigApp) {

    }

    getAllCluster() {
        let headers = new HttpHeaders({
            'Authorization': `${Utils.getCookie('token_type')} ${Utils.getCookie('access_token')}`
        });

        return this.http.get(
            this.config.urlBackEnd + 'cluster', { headers }
        )
    }

    createCluster(clusetr: ICluster) {
        let headers = new HttpHeaders({
            'Authorization': `${Utils.getCookie('token_type')} ${Utils.getCookie('access_token')}`
        });

        return this.http.post(
            this.config.urlBackEnd + 'cluster', { name: clusetr.name, description: clusetr.description, initfile_name: clusetr.initfile }, { headers }
        )
    }

    addHostToCluster(nameCluster: string, host: IHost, group: string | null, extid: string) {
        let headers = new HttpHeaders({
            'Authorization': `${Utils.getCookie('token_type')} ${Utils.getCookie('access_token')}`
        });

        return this.http.post(
            this.config.urlBackEnd + 'cluster/host', { name_cluster: nameCluster, host: host, group: group, extid_service: extid }, { headers }
        )
    }

    saveHost(nameCluster: string, extidService: string) {
        let headers = new HttpHeaders({
            'Authorization': `${Utils.getCookie('token_type')} ${Utils.getCookie('access_token')}`
        });

        return this.http.post(
            this.config.urlBackEnd + 'cluster/host/save?name_cluster=' + nameCluster + '&extid_service=' + extidService, { "name_cluster": nameCluster }, { headers }
        )
    }

    getListConfg(clusterName: string) {
        let headers = new HttpHeaders({
            'Authorization': `${Utils.getCookie('token_type')} ${Utils.getCookie('access_token')}`
        });

        return this.http.get(
            this.config.urlBackEnd + 'cluster/conf/list?cluster_name=' + clusterName, { headers }
        )
    }

    updateConfigFile(clusterName: string, configName: string | null, configFile: string | null) {
        let headers = new HttpHeaders({
            'Authorization': `${Utils.getCookie('token_type')} ${Utils.getCookie('access_token')}`
        });

        return this.http.post(
            this.config.urlBackEnd + 'cluster/conf/update', { cluster_name: clusterName, config_name: configName, config_file: configFile }, { headers }
        );
    }

    runAction(clusterName: string, extid: string, extidService: string, shellParameters: any) {
        let headers = new HttpHeaders({
            'Authorization': `${Utils.getCookie('token_type')} ${Utils.getCookie('access_token')}`
        });

        return this.http.post(
            this.config.urlBackEnd + 'task/run_action', { 'cluster_name': clusterName, 'extid': extid, 'shell_parameters': shellParameters, 'extid_service': extidService }, { headers }
        )
    }

    deleteCluster(clusterName: string | null) {
        let headers = new HttpHeaders({
            'Authorization': `${Utils.getCookie('token_type')} ${Utils.getCookie('access_token')}`
        });

        return this.http.post(
            this.config.urlBackEnd + 'cluster/delete?clusterName=' + clusterName, {}, { headers }
        );
    }
}