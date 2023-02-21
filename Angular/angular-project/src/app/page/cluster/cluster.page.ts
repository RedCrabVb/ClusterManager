import { Component, OnInit } from "@angular/core";
import { ModalService } from "src/app/components/modal/modalService";
import { ICluster } from "src/app/date/ICluster";
import { IInitFile } from "src/app/date/IInitfile";
import { ClusterService } from "src/app/services/cluster.service";
import { InitFileService } from "src/app/services/initfile.service";
import { cluster as data } from 'src/app/date/cluster';
import { InitFile as dataInit } from 'src/app/date/initfile';
import { FormControl } from "@angular/forms";
import { ClusterObject } from "src/app/date/clusterobject/clusterobject";
import { IHost } from "src/app/date/IHost";
import { HostsService } from "src/app/services/hosts.service";
import { ClusterData } from "src/app/date/clusterobject/clusterdata";
import { IConfig } from "src/app/date/clusterobject/IConfig";
import { HttpErrorResponse } from "@angular/common/http";
import { catchError, throwError } from "rxjs";

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
    templateUrl: './cluster.page.html'
})
export class ClusterComponenet implements OnInit {
    initfiles: IInitFile[] = dataInit;
    hosts: IHost[];
    configs: IConfig[];
    clusterObjects: ClusterObject[];
    cluseters: ICluster[] = data;

    name = new FormControl('');
    description = new FormControl('');
    initfile = new FormControl('');

    currentConfig = new FormControl('');
    currentConfigContent = new FormControl('');

    clusterObject: ClusterObject;
    selectServiceInClusterObject = new FormControl('');
    serviceDecriptionVar: ServiceDecriptionFormControll[] = []

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
            .pipe(catchError(this.handleError))
            .subscribe((res: any) => {
                this.initfiles = res;
            });
        this.clusterService.getAllCluster()
            .pipe(catchError(this.handleError))
            .subscribe((res: any) => {
                this.cluseters = res;
                this.clusterObjects = res;
                this.clusterObject = res[0];
            });
        this.hostsService.getAllHosts()
            .pipe(catchError(this.handleError))
            .subscribe((res: any) => {
                this.hosts = res;
            });
    }

    private handleError(error: HttpErrorResponse) {
        if (error.status === 0) {
            console.error('An error occurred:', error.error);
            alert('An error occurred: ' + error.message);
        } else {
            console.error(
                `Backend returned code ${error.status}, body was: `, error.error);

            alert(`Backend returned code ${error.status}, body was: ` + error.message);
        }
        return throwError(() => new Error('Something bad happened; please try again later.'));
    }


    runAction(extid: string) {
        let serviceClusterData = this.clusterObject.data.find(d => d.name == this.selectServiceInClusterObject.value);
        var actions = serviceClusterData?.actions.find(a => a.extid)?.extid;
        var shellParameters: any = {};
        this.serviceDecriptionVar.forEach(e => {
            shellParameters[e.nameDescription] = e.formControll.value;
        })
        if (actions != undefined && serviceClusterData != undefined) {
            this.clusterService.runAction(this.clusterObject.name, actions, serviceClusterData?.extid, shellParameters)
                .pipe(catchError(this.handleError))
                .subscribe(res => console.log(res));
        }
    }

    getVarService() {
        let vars_service = this.clusterObject.data.find(d => d.name == this.selectServiceInClusterObject.value)?.vars_service;
        vars_service?.forEach((var_service) => {
            var_service.description.forEach((descrit) => {
                if (this.serviceDecriptionVar.find(s => s.extid == var_service.extid && s.nameDescription == descrit) == undefined) {
                    this.serviceDecriptionVar.push(new ServiceDecriptionFormControll(descrit, var_service.extid, new FormControl()));
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
                    alert("Связка прошла успешно");
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
                .pipe(catchError(this.handleError))
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
                .pipe(catchError(this.handleError))
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
            .pipe(catchError(this.handleError))
            .subscribe((res: any) => {
                console.log(res);
                this.clusterService.getListConfg(this.clusterObject.name).subscribe((res: any) => {
                    console.log(res);
                    this.configs = res;
                });
            })
    }

    deleteCluster(nameCluster: string | null) {
        this.clusterService.deleteCluster(nameCluster).subscribe((res: any) => { console.log(res); this.ngOnInit(); })
    }

    createCluseter() {
        console.log({ "n": this.name.value, "d": this.description.value, "i": this.initfile.value })

        const cluseterNew: ICluster = {
            "name": this.name.value,
            "description": this.name.value,
            "initfile": this.initfile.value
        }
        this.clusterService.createCluster(cluseterNew)
            .pipe(catchError(this.handleError))
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