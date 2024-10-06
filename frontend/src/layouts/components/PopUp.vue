<script>
    export default{
        methods:{
            close(){
                this.$emit('close');
            }
        }


    }


</script>

<template>

    <div class="pop-up">
        <div class="pop-up-inner">
            <div class="pop-up-close" @click="close()">
                &times;
            </div>
           <slot></slot>

            <!-- <button class="btn" @click="close()">
                Close pop up
            </button> -->
        </div>
    </div>

</template>

<style lang="scss" scoped>
.pop-up{
        position:fixed;
        top: 0;
        left: 0;
        z-index: 1500;
        padding: 32px 16px 120px;
        height: 100vh;
        width: 100%;
        background-color: rgba($color: #52a07e, $alpha: 0.5);
        display: grid;
        place-items: center;

        &-close{
            position: absolute;
            height: 52px;
            width: 52px;
            display: flex;
            justify-content: center;
            align-items: center;
            top: 0;
            right: 0;
            font-size: 3rem;
            color: #d6d6d6;
            cursor: pointer;
        }

        &-inner{
            background-color: #fff;
            color: #000;
            position: relative;
            width: 90%;
            padding: 40px;
            border-radius: 8px;
            z-index: 999;
            height: 90vh;
            overflow-y: auto;
            box-shadow: 0 5px 5px rgba($color: #000, $alpha: 0.2);
            transition: all 250ms ease-in-out;
        }
    }

    .fade-enter,
    .fade-leave-to{
        opacity: 0;

        .pop-up-inner{
            opacity: 0;
            transform: translateY(-32px);
        }
    }

    .fade-enter-active,
    .fade-leave-active{
        transition: all 250ms ease-in-out;
    }

    .fade-leave-active,
    .fade-enter-active{
        transition-delay: 250ms;
    }
</style>