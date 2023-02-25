import { Component, Input, OnInit } from '@angular/core';
import { HostsService } from 'src/app/services/hosts.service';
import { ModalService } from 'src/app/components/modal/modalService';
import { IHost } from 'src/app/date/IHost';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { catchError, throwError } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';

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

    ngOnInit(): void {
        this.chnageHostControl({username: '', hostname: '', password: '', private_key: ''});
        this.chnageHostViewControl({username: '', hostname: '', password: '', private_key: ''});
        this.hostControl.valueChanges.subscribe((host) => console.log(host))

        this.hostsService.getAllHosts()
            .pipe(catchError(this.handleError))
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
        this.hostsService.deleteHost(host).subscribe((res) => {
            console.log(res);
            this.hostsService.getAllHosts().subscribe((res: any) => {
                this.hosts = res;
            })
        });

    }


    openHost(host: IHost) {
        this.chnageHostViewControl(host);
        this.openModal('custom-modal-2');
    }

    addHost() {
        this.hostsService.addHosts(this.hostControl.value)
            .pipe(catchError(this.handleError))
            .subscribe((res: any) => {
                alert(res.Status == 'Ok' ? 'Хост добавлен' : 'Ошибка ' + res['Status']);
                console.log(res);

                this.hostsService.getAllHosts().subscribe((res: any) => {
                    this.hosts = res;
                    
                    this.chnageHostViewControl(this.hostControl.value);
                    this.chnageHostControl({username: '', hostname: '', password: '', private_key: ''});

                    this.closeModal('custom-modal-1');
                    this.openModal('custom-modal-2');
                })

            });
    }

    testConnection(host: IHost) {
        console.log('test connection');
        // const currentHost = this.hostControl.value;
        this.hostsService.testConnection(host)
            .pipe(catchError(this.handleError))
            .subscribe((res: any) => {
                console.log(res); 
                alert(res.Status == true ?
                    'The connection is established: ' + host.hostname
                    : 'Failed to connect to the server: ' + host.hostname)
            })
    }


    openModal(id: string) {
        this.modalService.open(id);
    }

    closeModal(id: string) {
        this.modalService.close(id);
    }
}