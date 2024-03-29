import { Component, OnInit } from "@angular/core";
import { ModalService } from "src/app/components/modal/modalService";
import { ICluster } from "src/app/date/ICluster";
import { IInitFile } from "src/app/date/IInitfile";
import { ClusterService } from "src/app/services/cluster.service";
import { InitFileService } from "src/app/services/initfile.service";
import { InitFile as dataInit } from 'src/app/date/initfile';
import { FormControl, FormGroup } from "@angular/forms";
import { ClusterObject } from "src/app/date/clusterobject/clusterobject";
import { IHost } from "src/app/date/IHost";
import { HostsService } from "src/app/services/hosts.service";
import { ClusterData } from "src/app/date/clusterobject/clusterdata";
import { IConfig } from "src/app/date/clusterobject/IConfig";
import { HttpErrorResponse } from "@angular/common/http";
import { catchError, throwError } from "rxjs";
import Swal from "sweetalert2";
import { Utils } from "src/app/services/utils";

class ServiceDecriptionFormControll {
    nameDescription: string;
    formControll: FormControl;
    extid: string;

    constructor(nameDescription: string, extid: string, formControll: FormControl) {
        this.nameDescription = nameDescription;
        this.formControll = formControll;
        this.extid = extid;
    }
}

@Component({
    selector: 'cluster-component',
    templateUrl: './cluster.page.html',
    styleUrls: ["./cluster.page.css"]
})
export class ClusterComponenet implements OnInit {
    initfiles: IInitFile[] = dataInit;
    hosts: IHost[];
    configs: IConfig[];
    clusterObjects: ClusterObject[];
    cluseters: ICluster[] = [];

    name = new FormControl('');
    description = new FormControl('');
    initfile = new FormControl('');

    currentConfig = new FormControl('');
    currentConfigContent = new FormControl('');

    clusterObject: ClusterObject;
    selectServiceInClusterObject = new FormControl('');
    serviceDecriptionVar: ServiceDecriptionFormControll[] = [];
    mainContent: FormGroup;

    service: ClusterData | null;

    serviceForm = new FormControl('');
    hostTargetAdd = new FormControl('');
    groupTragetAdd = new FormControl('');

    addHostWindows: boolean = false;
    editConfig: boolean = false;
    runaction: boolean = false;
    main: boolean = true;


    constructor(private initFileService: InitFileService, private clusterService: ClusterService, private hostsService: HostsService, private modalService: ModalService) {
        this.serviceForm.valueChanges.subscribe((res) => {
            this.clusterObject.data.forEach((c) => {
                if (c.extid == res && (this.addHostWindows && c.requirements_groups != null)) {
                    this.service = c;
                } else {
                    this.service = null;
                }
            });
        })
    }

    ngOnInit(): void {
        this.initFileService.getAllInitfiles()
            .pipe(catchError(Utils.handleError))
            .subscribe((res: any) => {
                this.initfiles = res;
            });
        this.clusterService.getAllCluster()
            .pipe(catchError(Utils.handleError))
            .subscribe((res: any) => {
                this.cluseters = res;
                this.clusterObjects = res;
                this.clusterObject = res[0];
            });
        this.hostsService.getAllHosts()
            .pipe(catchError(Utils.handleError))
            .subscribe((res: any) => {
                this.hosts = res;
            });
    }


    runAction(extid: string) {
        let serviceClusterData = this.clusterObject.data.find(d => d.name == this.selectServiceInClusterObject.value);
        var actions = serviceClusterData?.actions.find(a => a.extid == extid)?.extid;
        var shellParameters: any = {};
        this.serviceDecriptionVar.filter(e => e.extid == extid).forEach(e => {
            shellParameters[e.nameDescription] = e.formControll.value;
        })
        if (actions != undefined && serviceClusterData != undefined) {
            this.clusterService.runAction(this.clusterObject.name, actions, serviceClusterData?.extid, shellParameters)
                .pipe(catchError(Utils.handleError))
                .subscribe((res: any) => {
                    window.location.href = '/proc_status?proc_id=' + res.ProcId;
                    console.log(res);
                });
        }
    }

    getVarService() {
        let vars_service = this.clusterObject.data.find(d => d.name == this.selectServiceInClusterObject.value)?.vars_service;
        vars_service?.forEach((var_service) => {
            var_service.description.forEach((description) => {
                if (!this.serviceDecriptionVar.find(s => s.extid == var_service.extid && s.nameDescription == description)) {
                    this.serviceDecriptionVar.push(new ServiceDecriptionFormControll(description, var_service.extid, new FormControl()));
                }
            })
        });

        return this.clusterObject.data.find(d => d.name == this.selectServiceInClusterObject.value)?.actions;
    }

    getServiceDescriptioOnExtId(extid: string) {
        return this.serviceDecriptionVar.filter(e => e.extid == extid);
    }

    whoHostGroupInCluster(type_host: string) {
        if (this.service == null) {
            return undefined;
        }
        for (let i in this.service.requirements_groups) {
            let itemI = this.service.requirements_groups[i];
            if (itemI.type_host == type_host) {
                let countInCluster = 0;
                for (let j in this.service.hosts) {
                    let itemJ = this.service.hosts[j];
                    if (itemJ.group == type_host) {
                        countInCluster += 1
                    }
                }
                return countInCluster;
            }
        }

        return 0

    }

    updateCluster() {
        this.clusterObjects.forEach((c) => {
            if (c.name == this.clusterObject.name && c.description == this.clusterObject.description) {
                this.clusterObject = c;
            }
            this.service = null;
            this.clusterObject.data.forEach((c) => {
                if (c.extid == this.serviceForm.value && (this.addHostWindows && c.requirements_groups != null)) {
                    this.service = c;
                }
            });
        })
    }

    addHostToCluster() {
        let username = this.hostTargetAdd.value?.split("|")[0]
        let hostname = this.hostTargetAdd.value?.split("|")[1]
        this.hosts.forEach((v: IHost) => {
            if (v.hostname == hostname && v.username == username && this.service != null) {
                this.clusterService.addHostToCluster(this.clusterObject.name, v, this.groupTragetAdd.value, this.service.extid).subscribe((res) => {
                    Swal.fire('Success', "The bundle was successful", 'success');
                    this.clusterService.getAllCluster().subscribe((res: any) => {
                        this.cluseters = res
                        this.clusterObjects = res

                    });
                })
            }
        })
    }

    saveHostInCluster() {
        if (this.service != null) {
            this.clusterService.saveHost(this.clusterObject.name, this.service?.extid)
                .pipe(catchError(Utils.handleError))
                .subscribe((res) => console.log(res))
        }
    }

    radioButton(nameButton: string) {
        this.addHostWindows = false;
        this.editConfig = false;
        this.runaction = false;
        this.main = false;

        if (nameButton == 'addHostWindows') {
            this.serviceForm.setValue('');
            this.addHostWindows = true;
        } else if (nameButton == 'editConfig') {

            this.editConfig = true;
            this.clusterService.getListConfg(this.clusterObject.name)
                .pipe(catchError(Utils.handleError))
                .subscribe((res: any) => {
                    console.log(res);
                    this.configs = res;
                });
        } else if (nameButton == 'runaction') {
            this.runaction = true;
        } else if (nameButton == 'main') {
            this.main = true;
        }
    }



    updateConfig(): void {
        this.clusterService
            .updateConfigFile(this.clusterObject.name, this.currentConfig.value, this.currentConfigContent.value)
            .pipe(catchError(Utils.handleError))
            .subscribe((res: any) => {
                console.log(res);
                this.clusterService.getListConfg(this.clusterObject.name).subscribe((res: any) => {
                    console.log(res);
                    this.configs = res;
                });
            })
    }

    deleteCluster(nameCluster: string | null) {


        Swal.fire({
            title: 'Are you sure?',
            text: 'Are you sure you want to delete the cluster?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes, delete it!',
            cancelButtonText: 'No, keep it',
        }).then((result) => {

            if (result.isConfirmed) {

                this.clusterService.deleteCluster(nameCluster).subscribe((res: any) => { console.log(res); this.ngOnInit(); })

            } else if (result.isDismissed) {

                console.log('Clicked No, cluster is safe!');

            }
        })


    }

    clusterDataToJson() {
        let newValue = JSON.stringify(this.clusterObject.data, null, "    ");
        if (this.mainContent == undefined || this.mainContent.controls['content'].value != newValue) {
            this.mainContent = new FormGroup({
                content: new FormControl(newValue)
            });
        }
        return this.mainContent ;
    }

    filterFunctionPackageConfiuration() {
        return this.initfiles.filter(b => b.license);
    }

    createCluseter() {
        console.log({ "n": this.name.value, "d": this.description.value, "i": this.initfile.value })

        const cluseterNew: ICluster = {
            "name": this.name.value,
            "description": this.name.value,
            "initfile": this.initfile.value
        }
        this.clusterService.createCluster(cluseterNew)
            .pipe(catchError(Utils.handleError))
            .subscribe((res) => {
                console.log(res)

                this.clusterService.getAllCluster().subscribe((res: any) => {
                    this.cluseters = res;
                    this.clusterObjects = res;
                })
            })
    }

    openCluster(cluster: ICluster) {

        this.clusterObjects.forEach((c) => {
            if (c.name == cluster.name && c.description == cluster.description) {
                this.clusterObject = c;
                this.radioButton('main');
            }
        });
    }

    openConfig(config: IConfig) {
        this.currentConfig.setValue(config.filename);
        this.currentConfigContent.setValue(config.content);
        this.openModal('custom-modal-editconfig');
    }

    openModal(id: string) {
        this.modalService.open(id);
    }

    closeModal(id: string) {
        this.modalService.close(id);
    }
}