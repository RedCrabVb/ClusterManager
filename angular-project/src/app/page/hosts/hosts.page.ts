import { Component, Input, OnInit } from '@angular/core';
import { HostsService } from 'src/app/services/hosts.service';
import { ModalService } from 'src/app/components/modal/modalService';
import { IHost } from 'src/app/date/IHost';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { catchError, throwError } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';
import Swal from 'sweetalert2';
import { Utils } from 'src/app/services/utils';

@Component({
    selector: 'app-hosts',
    templateUrl: './hosts.page.html',
})
export class HostsComponent implements OnInit {
    hosts: IHost[] = [];

    hostControl: FormGroup;
    hostViewControl: FormGroup;

    constructor(private hostsService: HostsService, private modalService: ModalService) {

    }

    ngOnInit(): void {
        this.chnageHostControl({ username: '', hostname: '', password: '', private_key: '' });
        this.chnageHostViewControl({ username: '', hostname: '', password: '', private_key: '' });
        this.hostControl.valueChanges.subscribe((host) => console.log(host))

        this.hostsService.getAllHosts()
            .pipe(catchError(Utils.handleError))
            .subscribe((res: any) => {
                console.log(res);
                this.hosts = res;
            });
    }

    chnageHostControl(host: IHost) {
        this.hostControl = new FormGroup({
            hostname: new FormControl(host.hostname, [Validators.required, Validators.minLength(1)]),
            username: new FormControl(host.username, [Validators.required, Validators.minLength(1)]),
            password: new FormControl(host.password),
            private_key: new FormControl(host.private_key)
        });
    }

    chnageHostViewControl(host: IHost) {
        this.hostViewControl = new FormGroup({
            hostname: new FormControl(host.hostname, [Validators.required, Validators.minLength(1)]),
            username: new FormControl(host.username, [Validators.required, Validators.minLength(1)]),
            password: new FormControl(host.password),
            private_key: new FormControl(host.private_key)
        });
    }

    deleteHost(host: IHost) {

        Swal.fire({
            title: 'Are you sure?',
            text: 'Are you sure you want to delete the host?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes, delete it!',
            cancelButtonText: 'No, keep it',
        }).then((result) => {

            if (result.isConfirmed) {

                this.hostsService.deleteHost(host).subscribe((res) => {
                    console.log(res);
                    this.hostsService.getAllHosts().subscribe((res: any) => {
                        this.hosts = res;
                    })
                });

            } else if (result.isDismissed) {

                console.log('Clicked No, host is safe!');

            }
        })



    }


    openHost(host: IHost) {
        this.chnageHostViewControl(host);
        this.openModal('custom-modal-2');
    }

    addHost() {
        this.hostsService.addHosts(this.hostControl.value)
            .pipe(catchError(Utils.handleError))
            .subscribe((res: any) => {
                res.Status == 'Ok' ? Swal.fire('success', 'Host add', 'success') : Swal.fire('Error', res['Status'], 'error');
                console.log(res);

                this.hostsService.getAllHosts().subscribe((res: any) => {
                    this.hosts = res;

                    this.chnageHostViewControl(this.hostControl.value);
                    this.chnageHostControl({ username: '', hostname: '', password: '', private_key: '' });

                    this.closeModal('custom-modal-1');
                    this.openModal('custom-modal-2');
                })

            });
    }

    testConnection(host: IHost) {
        console.log('test connection');
        this.hostsService.testConnection(host)
            .pipe(catchError(Utils.handleError))
            .subscribe((res: any) => {
                console.log(res);

                res.Status == true ? Swal.fire('success', 'The connection is established: ' + host.hostname, 'success') :
                    Swal.fire('error', 'Failed to connect to the server: ' + host.hostname, 'error');
            })
    }


    openModal(id: string) {
        this.modalService.open(id);
    }

    closeModal(id: string) {
        this.modalService.close(id);
    }
}