import { Component, OnInit } from "@angular/core";
import { ModalService } from "src/app/components/modal/modalService";
import { ICluster } from "src/app/date/ICluster";
import { IInitFile } from "src/app/date/IInitfile";
import { ClusterService } from "src/app/services/cluster.service";
import { InitFileService } from "src/app/services/initfile.service";
import {cluster as data } from 'src/app/date/cluster';
import {InitFile as dataInit } from 'src/app/date/initfile';
import { FormControl } from "@angular/forms";

@Component({
    selector: 'cluster-component',
    templateUrl: './cluster.page.html'
})
export class ClusterComponenet implements OnInit {
    initfiles: IInitFile[] = dataInit;
    cluseters: ICluster[] = data;

    name = new FormControl('');
    description = new FormControl('');
    initfile = new FormControl('');
    
    constructor(private initFileService: InitFileService, private clusterService: ClusterService, private modalService: ModalService) {

    }

    ngOnInit(): void {
        this.initFileService.getAllInitfiles().subscribe((res: any) =>{
            this.initfiles = res
        })
        this.clusterService.getAllCluster().subscribe((res: any) => {
            this.cluseters = res
        })
    }

    createCluseter() {
        console.log({"n": this.name.value, "d": this.description.value, "i": this.initfile.value})

        const cluseterNew: ICluster = {
            "name": this.name.value, 
            "description": this.name.value, 
            "initfile": this.initfile.value
        }
        this.clusterService.createCluster(cluseterNew).subscribe((res) => {
            console.log(res)

            this.clusterService.getAllCluster().subscribe((res: any) => {
                this.cluseters = res
            })
        })
    }

    openModal(id: string) {
        this.modalService.open(id);
    }

    closeModal(id: string) {
        this.modalService.close(id);
    }
}