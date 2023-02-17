import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { ConfigApp } from "./config";
import { ICluster } from "../date/ICluster";
import { IHost } from "../date/IHost";

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

    addHostToCluster(nameCluster: string, host: IHost, group: string | null, extid: string) {
        return this.http.post(
            this.config.urlBackEnd + 'cluster/host', {name_cluster: nameCluster, host: host, group: group, extid_service: extid}
        )
    }

    saveHost(nameCluster: string, extidService: string) {
        return this.http.post(
            this.config.urlBackEnd + 'cluster/host/save?name_cluster=' + nameCluster + '&extid_service=' + extidService, {"name_cluster": nameCluster}
        )
    }

    getListConfg(clusterName: string) {
        return this.http.get(
            this.config.urlBackEnd + 'cluster/conf/list?cluster_name=' + clusterName 
        )
    }

    updateConfigFile(clusterName: string, configName: string | null, configFile: string | null) {
        return this.http.post(
            this.config.urlBackEnd + 'cluster/conf/update', {cluster_name: clusterName, config_name: configName, config_file: configFile}
        );
    }

    runAction(clusterName: string, extid: string, shellParameters: any) {
        return this.http.post(
            this.config.urlBackEnd + 'task/run_action', {'cluster_name': clusterName, 'extid': extid, 'shell_parameters': shellParameters}
        )
    }
}